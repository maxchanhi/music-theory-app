const express = require('express');
const router = express.Router();
const path = require('path');

const orchestratorPath = path.resolve(__dirname, '..', 'services', 'orchestrator');
const { processMessage } = require(orchestratorPath);
const memory = require('../services/memory');

// Session states: IDLE | QUESTION_ASKED | WAITING

function getSession(userId) {
  return memory.load(userId);
}

router.get('/', (req, res) => {
  const userId = (req.session && req.session.userInfo && req.session.userInfo.user_id) || 'anonymous';
  const session = memory.load(userId);
  res.render('tutor', {
    user: req.session.userInfo || null,
    userId,
    title: 'AI Music Tutor',
    savedHistory: JSON.stringify(session.history || [])
  });
});

router.post('/api/message', async (req, res) => {
  try {
    const { message, mode } = req.body;
    const userId = (req.session && req.session.userInfo && req.session.userInfo.user_id) || 'anonymous';

    if (!message) return res.status(400).json({ error: 'Message is required' });

    const session = getSession(userId);

    const progress = {
      level: session.progress.level,
      weakAreas: session.progress.weakAreas,
      strongAreas: session.progress.strongAreas,
      totalQuestions: session.progress.totalQuestions
    };

    // Pass current question data as pendingQuestion so orchestrator can
    // detect answers and fallback to direct checking if needed
    const pendingQuestion = session.state === 'QUESTION_ASKED' ? session.currentQuestionData : null;

    const result = await processMessage(userId, message, session.history, progress, pendingQuestion);

    // Update session history
    session.history.push(
      { role: 'user', content: message },
      { role: 'assistant', content: result.reply }
    );

    // ---- State machine ----
    let freshDisplayData = null;
    if (result.toolCalls && result.toolCalls.length > 0) {
      for (const tc of result.toolCalls) {
        if (tc.name === 'generate_question') {
          session.state = 'QUESTION_ASKED';
          const genStep = (result.steps || []).find(s =>
            s.toolCalls && s.toolCalls.some(t => t.name === 'generate_question')
          );
          if (genStep && genStep.results) {
            let qData = genStep.results[0];
            // If safeJSON fallback returned raw string, try parsing again
            if (typeof qData === 'string') {
              try { qData = JSON.parse(qData); } catch(e) { qData = null; }
            }
            if (qData && typeof qData === 'object') {
              session.currentQuestionData = qData;
              session.currentQuestionData.topic = tc.args.topic;
              freshDisplayData = qData.displayData;
            }
          }
        }

        if (tc.name === 'check_answer') {
          session.state = 'IDLE';
          session.currentQuestionData = null;
          session.progress.totalQuestions++;

          // Determine if correct from step results
          const checkStep = (result.steps || []).find(s =>
            s.toolCalls && s.toolCalls.some(t => t.name === 'check_answer')
          );
          if (checkStep && checkStep.results && checkStep.results[0]) {
            const checkResult = checkStep.results[0];
            if (checkResult.correct) {
              session.progress.correctCount++;
              session.progress.strongAreas.push(tc.args.topic);
            } else {
              session.progress.weakAreas.push(tc.args.topic);
            }
          }
        }
      }
    } else {
      session.state = 'IDLE';
      session.currentQuestionData = null;
    }

    // Persist session to disk so history survives restarts
    memory.save(userId, session);

    // Include displayData from current question for score rendering
    const displayData = freshDisplayData || session.currentQuestionData?.displayData || null;

    res.json({
      reply: result.reply,
      mode: mode || 'text',
      toolCalls: result.toolCalls,
      steps: result.steps || [],
      metrics: result.metrics || {},
      state: session.state,
      topic: session.currentQuestionData?.topic || null,
      displayData
    });

  } catch (err) {
    console.error('Tutor API error:', err);
    res.status(500).json({ error: 'Failed to process message' });
  }
});

router.post('/api/reset', (req, res) => {
  const userId = (req.session && req.session.userInfo && req.session.userInfo.user_id) || 'anonymous';
  memory.save(userId, {
    history: [],
    state: 'IDLE',
    currentQuestionData: null,
    progress: { level: 'beginner', weakAreas: [], strongAreas: [], totalQuestions: 0, correctCount: 0 }
  });
  res.json({ status: 'reset' });
});

module.exports = router;
