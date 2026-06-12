const path = require('path');

const registryPath = path.resolve(__dirname, '..', 'logic', 'registry');
const registry = require(registryPath);

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY || process.env.LLM_API_KEY;
const DEEPSEEK_BASE_URL = process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com/v1';
const LLM_MODEL = process.env.LLM_MODEL || 'deepseek-chat';

const MAX_STEPS = 6;
const topics = registry.listTopics();

const SYSTEM_PROMPT_BASE = `You are a music theory tutor named Melody. You help students learn and practice music theory.

## Available Topics
${topics.map(t => `- ${t.topic}: ${t.name} (${t.description})`).join('\n')}

## Tools You Can Use
You have 5 tools available:
1. generate_question(topic, difficulty) - Create a quiz question
2. check_answer(topic, questionData, userAnswer) - Verify student's answer
3. list_topics() - Show all available topics
4. get_progress(user_id) - Get student performance data
5. save_feedback(user_id, topic, user_answer, correct_answer, was_correct) - Save progress

## CRITICAL RULES
1. Keep responses SHORT (1-2 sentences) — they will be spoken via TTS
2. Ask ONE question at a time
3. To present a quiz question you MUST call generate_question first. NEVER write a quiz question in plain text without calling generate_question.
4. When a student gives an answer, you MUST call check_answer with the questionData you received from generate_question. NEVER say "let me check" without actually calling the tool.
5. After calling check_answer, give brief feedback then ask if they want another or a new topic
6. Use get_progress when asked about performance
7. Be encouraging. Brief praise for correct, short hint for wrong
8. If they ask a general theory question, answer it conversationally`;

const TOOL_DEFS = topics.length > 0 ? [
  {
    type: 'function',
    function: {
      name: 'generate_question',
      description: 'Generate a music theory practice question on a specific topic',
      parameters: {
        type: 'object',
        properties: {
          topic: {
            type: 'string',
            enum: topics.map(t => t.topic),
            description: 'Topic to quiz on'
          },
          difficulty: {
            type: 'string',
            description: 'Optional difficulty level for the topic'
          }
        },
        required: ['topic']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'check_answer',
      description: 'Check if a student answer is correct using the questionData from generate_question',
      parameters: {
        type: 'object',
        properties: {
          topic: { type: 'string', description: 'Topic of the question' },
          questionData: { type: 'object', description: 'The full question data object that was returned by generate_question' },
          userAnswer: { type: 'string', description: 'The student answer text' }
        },
        required: ['topic', 'questionData', 'userAnswer']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'list_topics',
      description: 'List all available music theory topics',
      parameters: { type: 'object', properties: {} }
    }
  },
  {
    type: 'function',
    function: {
      name: 'get_progress',
      description: 'Get student performance data from the database',
      parameters: {
        type: 'object',
        properties: { user_id: { type: 'string', description: 'The user ID' } },
        required: ['user_id']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'save_feedback',
      description: 'Save progress feedback about a student answer',
      parameters: {
        type: 'object',
        properties: {
          user_id: { type: 'string' },
          topic: { type: 'string' },
          user_answer: { type: 'string' },
          correct_answer: { type: 'string' },
          was_correct: { type: 'boolean' }
        },
        required: ['user_id', 'topic', 'user_answer', 'correct_answer', 'was_correct']
      }
    }
  }
] : [];

// ==============================

async function callLLM(messages, options = {}) {
  // Judge mode: no tools, minimal tokens, for yes/no judgments
  if (options.judgeMode) {
    const response = await fetch(`${DEEPSEEK_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${DEEPSEEK_API_KEY}` },
      body: JSON.stringify({ model: LLM_MODEL, messages, temperature: 0, max_tokens: 10 })
    });
    if (!response.ok) throw new Error(`Judge LLM error ${response.status}`);
    return response.json();
  }

  const body = {
    model: LLM_MODEL,
    messages,
    tools: TOOL_DEFS,
    tool_choice: 'auto',
    temperature: 0.7,
    max_tokens: 4096
  };

  // Inject a system instruction to force tool calling when needed
  if (options.forceTool) {
    body.messages = [
      ...messages,
      { role: 'system', content: 'The user just answered a quiz question. You MUST call check_answer NOW with the questionData from your previous generate_question call. Do not explain — call the function immediately.' }
    ];
  }

  const response = await fetch(`${DEEPSEEK_BASE_URL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
    },
    body: JSON.stringify(body)
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`LLM API error ${response.status}: ${text}`);
  }
  return response.json();
}

function safeJSON(str, fallback = {}) {
  try { return JSON.parse(str || '{}'); } catch { return fallback; }
}

// Ask the LLM to judge if a student answer is semantically equivalent
async function judgeAnswer(topic, questionData, userAnswer) {
  const correctAnswer = questionData.correctAnswer;
  const questionText = questionData.questionText || '';
  try {
    const data = await callLLM([
      { role: 'system', content: 'You are a music theory answer judge. Determine if the student answer is semantically correct. Consider: abbreviations (maj=Major, min=Minor, aug=Augmented, dim=Diminished, per=Perfect, perf=Perfect, dom=Dominant, nat=Natural), case differences, number shorthand (3rd=Third, 7th=Seventh), and extra words. Answer ONLY "yes" or "no".' },
      { role: 'user', content: `Question: ${questionText}\nCorrect answer: ${correctAnswer}\nStudent answer: ${userAnswer}\n\nIs the student correct? (yes/no)` }
    ], { judgeMode: true });
    const judgeText = data.choices[0].message.content?.trim().toLowerCase() || '';
    const isCorrect = judgeText === 'yes' || judgeText.startsWith('y');
    return {
      correct: isCorrect,
      correctAnswer: String(correctAnswer),
      explanation: isCorrect
        ? `Correct! ${correctAnswer} is right (accepting "${userAnswer}"). Would you like another question?`
        : `The correct answer is ${correctAnswer}. Would you like to try another one?`
    };
  } catch (e) {
    console.warn('Judge LLM call failed:', e.message);
    return null;
  }
}

async function executeTool(toolCall) {
  const fnName = toolCall.function.name;
  const args = safeJSON(toolCall.function.arguments);

  switch (fnName) {
    case 'list_topics':
      return JSON.stringify(topics.map(t => `${t.topic}: ${t.name} - ${t.description}`));

    case 'generate_question': {
      const options = {};
      if (args.difficulty) options.difficulty = args.difficulty;
      const question = registry.generateQuestion(args.topic, options);
      return JSON.stringify(question);
    }

    case 'check_answer': {
      if (!args.questionData) {
        return JSON.stringify({ correct: false, correctAnswer: 'unknown', explanation: 'No question data provided. Please generate a new question.' });
      }
      const result = registry.checkAnswer(args.topic, args.questionData, args.userAnswer);
      if (result.correct) return JSON.stringify(result);

      // Exact match failed — ask LLM to judge semantic equivalence
      try {
        const judge = await judgeAnswer(args.topic, args.questionData, args.userAnswer);
        if (judge && judge.correct) return JSON.stringify(judge);
      } catch (e) { /* fall through */ }

      return JSON.stringify(result);
    }

    case 'get_progress': {
      try {
        const fbPath = path.resolve(__dirname, '..', 'logic', 'feedback');
        const fb = require(fbPath);
        const list = await fb.getFeedbackByUserId(args.user_id);
        const wrong = list.filter(f => f.details && f.details.includes('Wrong')).length;
        return JSON.stringify({
          totalQuestions: list.length,
          correct: list.length - wrong,
          wrong,
          recentTopics: [...new Set(list.map(f => f.subject))]
        });
      } catch (e) {
        return JSON.stringify({ error: 'Database unavailable', totalQuestions: 0, correct: 0, wrong: 0 });
      }
    }

    case 'save_feedback': {
      try {
        const fbPath = path.resolve(__dirname, '..', 'logic', 'feedback');
        const { Feedback } = require(fbPath);
        const doc = new Feedback({
          user_id: args.user_id,
          subject: `${args.topic} quiz`,
          details: `[('${args.was_correct ? 'Correct' : 'Wrong'}', '${args.user_answer}', '${args.correct_answer}')]`,
          date: new Date()
        });
        await doc.save();
        return JSON.stringify({ saved: true });
      } catch (e) {
        return JSON.stringify({ saved: false, error: e.message });
      }
    }

    default:
      return JSON.stringify({ error: `Unknown tool: ${fnName}` });
  }
}

// Direct answer checking fallback when LLM refuses to use check_answer
async function fallbackAnswerCheck(pendingQuestion, userMessage) {
  // Use the registry's real checkAnswer if we know the topic
  const topic = pendingQuestion.topic;
  if (topic && registry.getModule(topic)) {
    try {
      const result = registry.checkAnswer(topic, pendingQuestion, userMessage);
      if (result.correct) return {
        correct: true,
        correctAnswer: result.correctAnswer,
        explanation: `Correct! ${result.explanation.replace(/^Correct[!]*\s*/i, '')} Would you like another question?`
      };
      // Exact match failed — try LLM judge
      const judge = await judgeAnswer(topic, pendingQuestion, userMessage);
      if (judge && judge.correct) return judge;
      if (judge) return judge;
      return {
        correct: false,
        correctAnswer: result.correctAnswer,
        explanation: `${result.explanation} Would you like to try another one?`
      };
    } catch (e) { /* fall through */ }
  }

  // Simple string comparison fallback
  const qData = pendingQuestion.rawData || pendingQuestion;
  const correctAnswer = pendingQuestion.correctAnswer || qData.answer || qData.correctAnswer;
  if (!correctAnswer) return null;

  const normalizedUser = userMessage.trim().toLowerCase().replace(/^a\s+/i, '');
  const normalizedCorrect = String(correctAnswer).trim().toLowerCase();

  const isCorrect = normalizedUser === normalizedCorrect;

  return {
    correct: isCorrect,
    correctAnswer: String(correctAnswer),
    explanation: isCorrect
      ? `Correct! The answer is ${correctAnswer}. Great work! Would you like another question?`
      : `Not quite — the correct answer is ${correctAnswer}. Would you like to try another one?`
  };
}

// ==============================
// Main agent loop — based on ReAct pattern from OpenAI Agents SDK / smolagents
// ==============================

async function processMessage(userId, message, history = [], progress = null, pendingQuestion = null) {
  const progressInfo = progress ? `Student level: ${progress.level || 'beginner'}
Questions answered: ${progress.totalQuestions || 0}
Weak areas: ${progress.weakAreas ? progress.weakAreas.join(', ') : 'none yet'}
Strong areas: ${progress.strongAreas ? progress.strongAreas.join(', ') : 'none yet'}` : 'New student - assess their level';

  const systemPrompt = `${SYSTEM_PROMPT_BASE}

## Current Student
${progressInfo}`;

  const messages = [
    { role: 'system', content: systemPrompt },
    ...(history || []).slice(-16),
    { role: 'user', content: message }
  ];

  const steps = [];
  const startTime = Date.now();
  const hasPendingQuestion = pendingQuestion !== null;
  const looksLikeAnswer = hasPendingQuestion && message.length < 80;

  let currentMsgs = messages;
  let finalReply = null;
  let forceTool = false;
  let toolCallsThisTurn = [];

  try {
    // --- Agent loop (max MAX_STEPS iterations) ---
    for (let step = 0; step < MAX_STEPS && finalReply === null; step++) {
      const data = await callLLM(currentMsgs, { forceTool });
      const choice = data.choices[0];
      const replyMsg = choice.message;
      const hadToolCalls = replyMsg.tool_calls && replyMsg.tool_calls.length > 0;

      // If tool calls were requested, execute them
      if (hadToolCalls) {
        const toolResults = [];
        for (const tc of replyMsg.tool_calls) {
          let result;
          try {
            result = await executeTool(tc);
          } catch (err) {
            console.error(`Tool error [${tc.function.name}]: ${err.message}`);
            result = JSON.stringify({ error: err.message });
          }
          toolResults.push({
            role: 'tool',
            tool_call_id: tc.id,
            content: result
          });
        }

        steps.push({
          step,
          toolCalls: replyMsg.tool_calls.map(tc => ({
            name: tc.function.name,
            args: safeJSON(tc.function.arguments)
          })),
          results: toolResults.map(r => safeJSON(r.content, r.content))
        });

        // Track which tools were called
        for (const tc of replyMsg.tool_calls) {
          toolCallsThisTurn.push(tc.function.name);
        }

        // Add messages and tool results to conversation for next iteration
        currentMsgs = [...currentMsgs, replyMsg, ...toolResults];
        forceTool = false;
        continue;

      } else {
        // No tool calls — retry with forced tool choice if a question is pending
        if (looksLikeAnswer && !toolCallsThisTurn.includes('check_answer') && !forceTool) {
          forceTool = true;
          continue;
        }

        // Force tool already tried or not applicable — do fallback check
        if (looksLikeAnswer && !toolCallsThisTurn.includes('check_answer')) {
          const fallback = await fallbackAnswerCheck(pendingQuestion, message);
          if (fallback) {
            finalReply = fallback.explanation;
            break;
          }
        }

        finalReply = replyMsg.content;
        break;
      }
    }

    // --- Fallback if loop exhausted without final reply ---
    if (finalReply === null) {
      if (looksLikeAnswer && !toolCallsThisTurn.includes('check_answer')) {
        const fallback = await fallbackAnswerCheck(pendingQuestion, message);
        if (fallback) {
          finalReply = fallback.explanation;
        } else {
          finalReply = "Let me help you with music theory. What would you like to practice?";
        }
      } else {
        finalReply = "Let me help you with music theory. What would you like to practice?";
      }
    }

    const elapsed = Date.now() - startTime;

    return {
      reply: finalReply,
      steps,
      toolCalls: toolCallsThisTurn.length > 0
        ? (() => {
            const seen = new Set();
            return steps.flatMap(s => s.toolCalls || []).filter(tc => {
              const key = tc.name + JSON.stringify(tc.args);
              if (seen.has(key)) return false;
              seen.add(key);
              return true;
            });
          })()
        : [],
      metrics: {
        totalSteps: steps.length,
        totalTimeMs: elapsed,
        toolCallsCount: steps.reduce((sum, s) => sum + (s.toolCalls ? s.toolCalls.length : 0), 0)
      }
    };

  } catch (err) {
    console.error('Orchestrator error:', err.message);

    // If LLM failed but we have a pending answer, use fallback
    let fallbackReply = null;
    if (looksLikeAnswer && !toolCallsThisTurn.includes('check_answer')) {
      const fb = await fallbackAnswerCheck(pendingQuestion, message);
      if (fb) fallbackReply = fb.explanation;
    }

    return {
      reply: fallbackReply || `The answer is ${pendingQuestion?.correctAnswer || '...'}. Let me know when you're ready for another question!`,
      toolCalls: [],
      steps,
      metrics: { totalSteps: steps.length, totalTimeMs: Date.now() - startTime, error: err.message }
    };
  }
}

module.exports = { processMessage };
