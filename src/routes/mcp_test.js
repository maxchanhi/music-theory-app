const express = require('express');
const router = express.Router();
const path = require('path');
const registry = require('../logic/registry');

// ── List all tools with their schemas ──────────────────────────
router.get('/tools', (_req, res) => {
  const topics = registry.listTopics();
  res.json({
    tools: [
      {
        name: 'generate_question',
        description: 'Generate a music theory practice question',
        parameters: {
          topic:        { type: 'string', required: true,  enum: topics.map(t => t.topic), desc: topics.map(t => `${t.name}: ${t.description}`).join(' | ') },
          difficulty:   { type: 'string', required: false, enum: [...new Set(topics.flatMap(t => t.difficultyLevels || []))], desc: 'Difficulty preset' },
          clefs:        { type: 'json', required: false, desc: 'Array of clefs to pick from: ["treble","bass"] — use one item for single clef' },
          accidentals:  { type: 'json', required: false, desc: 'Array: ["Sharp (♯)","Natural (♮)","Flat (♭)","Double-sharp(x)","Double-flat(♭♭)"]' },
          sameClef:     { type: 'boolean', required: false, desc: 'Both staves use same clef (interval)' },
          compound:     { type: 'boolean', required: false, desc: 'Allow compound intervals (different octaves)' },
          clef:         { type: 'string', required: false, enum: ['treble','bass','alto','tenor'], desc: 'Pick a specific clef (clef_minor only)' },
          sharps:       { type: 'string', required: false, desc: 'Key sharps/flats: 0-6 positive=sharps, negative=flats (clef_minor only)' },
        }
      },
      {
        name: 'check_answer',
        description: 'Check a student answer against question data',
        parameters: {
          topic:        { type: 'string', required: true, enum: topics.map(t => t.topic) },
          questionData: { type: 'json',    required: true, desc: 'Full JSON returned by generate_question' },
          userAnswer:   { type: 'string',  required: true, desc: 'Student answer text' },
        }
      },
      {
        name: 'list_topics',
        description: 'List all available topics',
        parameters: {}
      },
      {
        name: 'get_progress',
        description: 'Get student progress',
        parameters: {
          user_id: { type: 'string', required: true }
        }
      },
      {
        name: 'save_feedback',
        description: 'Save quiz feedback',
        parameters: {
          user_id:       { type: 'string', required: true },
          topic:         { type: 'string', required: true },
          user_answer:   { type: 'string', required: true },
          correct_answer:{ type: 'string', required: true },
          was_correct:   { type: 'boolean', required: true },
        }
      }
    ],
    topics: topics.map(t => ({ topic: t.topic, name: t.name, description: t.description, difficultyLevels: t.difficultyLevels }))
  });
});

// ── Execute a tool directly ─────────────────────────────────────
router.post('/execute', async (req, res) => {
  try {
    const { tool, args } = req.body;
    if (!tool) return res.status(400).json({ error: 'Missing tool name' });

    switch (tool) {
      case 'generate_question': {
        const options = {};
        if (args.difficulty) options.difficulty = args.difficulty;
        if (args.clefs) options.clefs = args.clefs;
        if (args.accidentals) options.accs = args.accidentals;
        if (args.sameClef !== undefined) options.sameClef = args.sameClef;
        if (args.compound !== undefined) options.compound = args.compound;
        if (args.clef) options.clef = args.clef;
        if (args.sharps !== undefined) options.sharps = args.sharps;
        const question = registry.generateQuestion(args.topic, options);
        return res.json({ result: question });
      }
      case 'check_answer': {
        const result = registry.checkAnswer(args.topic, args.questionData, args.userAnswer);
        return res.json({ result });
      }
      case 'list_topics': {
        return res.json({ result: registry.listTopics() });
      }
      case 'get_progress': {
        const fbPath = path.resolve(__dirname, '..', 'logic', 'feedback');
        const fb = require(fbPath);
        const list = await fb.getFeedbackByUserId(args.user_id);
        const wrong = list.filter(f => f.details && f.details.includes('Wrong')).length;
        return res.json({ result: { totalQuestions: list.length, correct: list.length - wrong, wrong, recentTopics: [...new Set(list.map(f => f.subject))] } });
      }
      case 'save_feedback': {
        const fbPath = path.resolve(__dirname, '..', 'logic', 'feedback');
        const { Feedback } = require(fbPath);
        const doc = new Feedback({
          user_id: args.user_id,
          subject: `${args.topic} quiz`,
          details: `[('${args.was_correct ? 'Correct' : 'Wrong'}', '${args.user_answer}', '${args.correct_answer}')]`,
          date: new Date()
        });
        await doc.save();
        return res.json({ result: { saved: true } });
      }
      default:
        return res.status(400).json({ error: `Unknown tool: ${tool}` });
    }
  } catch (err) {
    console.error('MCP execute error:', err);
    res.status(500).json({ error: err.message });
  }
});

// ── Serve the test page ─────────────────────────────────────────
router.get('/', (_req, res) => {
  res.sendFile(path.resolve(__dirname, '..', 'views', 'mcp_test.html'));
});

module.exports = router;
