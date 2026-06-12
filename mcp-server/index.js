const path = require('path');

// Resolve path to src/logic/registry
const registryPath = path.resolve(__dirname, '..', 'src', 'logic', 'registry');
const registry = require(registryPath);

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendMessage(msg) {
  process.stdout.write(JSON.stringify(msg) + '\n');
}

// Tool definitions
const TOOLS = [
  {
    name: 'generate_question',
    description: 'Generate a music theory practice question on a given topic with optional difficulty',
    inputSchema: {
      type: 'object',
      properties: {
        topic: {
          type: 'string',
          description: 'Topic name (e.g. interval, pitch_id, chromatic, inversion)'
        },
        difficulty: {
          type: 'string',
          description: 'Optional difficulty level (topic-dependent)'
        }
      },
      required: ['topic']
    }
  },
  {
    name: 'check_answer',
    description: 'Check if the user answer is correct for a previously generated question',
    inputSchema: {
      type: 'object',
      properties: {
        topic: { type: 'string' },
        questionData: { type: 'object' },
        userAnswer: { type: 'string', description: 'The student answer' }
      },
      required: ['topic', 'questionData', 'userAnswer']
    }
  },
  {
    name: 'list_topics',
    description: 'List all available music theory topics with descriptions and difficulty levels',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'get_progress',
    description: 'Get student progress data from the feedback database',
    inputSchema: {
      type: 'object',
      properties: {
        user_id: { type: 'string', description: 'The user ID' }
      },
      required: ['user_id']
    }
  },
  {
    name: 'save_feedback',
    description: 'Save feedback about a student answer for progress tracking',
    inputSchema: {
      type: 'object',
      properties: {
        user_id: { type: 'string' },
        topic: { type: 'string' },
        question: { type: 'string' },
        user_answer: { type: 'string' },
        correct_answer: { type: 'string' },
        was_correct: { type: 'boolean' }
      },
      required: ['user_id', 'topic', 'user_answer', 'correct_answer', 'was_correct']
    }
  }
];

async function handleToolCall(request) {
  const toolName = request.params.name;
  const args = request.params.arguments || {};

  try {
    let result;

    switch (toolName) {
      case 'list_topics': {
        result = registry.listTopics();
        break;
      }

      case 'generate_question': {
        const { topic, difficulty } = args;
        if (!topic) throw new Error('topic is required');

        const options = {};
        if (difficulty) options.difficulty = difficulty;

        const question = registry.generateQuestion(topic, options);

        // Remove rawData from the response to keep it clean
        const { rawData, ...safeQuestion } = question;
        result = safeQuestion;
        break;
      }

      case 'check_answer': {
        const { topic, questionData, userAnswer } = args;
        if (!topic || !questionData || userAnswer === undefined) {
          throw new Error('topic, questionData, and userAnswer are required');
        }

        const checkResult = registry.checkAnswer(topic, questionData, userAnswer);
        result = checkResult;
        break;
      }

      case 'get_progress': {
        const { user_id } = args;
        if (!user_id) throw new Error('user_id is required');

        // Try to load feedback module dynamically (MongoDB may not be available)
        try {
          const feedbackPath = path.resolve(__dirname, '..', 'src', 'logic', 'feedback');
          const feedback = require(feedbackPath);
          const feedbackList = await feedback.getFeedbackByUserId(user_id);

          // Calculate basic stats
          const total = feedbackList.length;
          const wrong = feedbackList.filter(f => f.details && f.details.includes('Wrong')).length;
          const correct = total - wrong;

          result = {
            user_id,
            totalQuestions: total,
            correct,
            wrong,
            recentFeedback: feedbackList.slice(0, 5)
          };
        } catch (dbErr) {
          console.error('Feedback DB error:', dbErr.message);
          result = {
            user_id,
            error: 'Database not available',
            totalQuestions: 0,
            correct: 0,
            wrong: 0
          };
        }
        break;
      }

      case 'save_feedback': {
        const { user_id, topic, question, user_answer, correct_answer, was_correct } = args;
        if (!user_id) throw new Error('user_id is required');

        try {
          const feedbackPath = path.resolve(__dirname, '..', 'src', 'logic', 'feedback');
          const { Feedback } = require(feedbackPath);

          const feedbackDoc = new Feedback({
            user_id,
            subject: `${topic} quiz`,
            details: `[('${was_correct ? 'Correct' : 'Wrong'}', '${user_answer}', '${correct_answer}')]`,
            date: new Date()
          });
          await feedbackDoc.save();
          result = { saved: true, id: feedbackDoc._id.toString() };
        } catch (dbErr) {
          console.error('Save feedback error:', dbErr.message);
          result = { saved: false, error: dbErr.message };
        }
        break;
      }

      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }

    sendMessage({
      jsonrpc: '2.0',
      id: request.id,
      result: { content: [{ type: 'text', text: JSON.stringify(result) }] }
    });

  } catch (err) {
    sendMessage({
      jsonrpc: '2.0',
      id: request.id,
      error: { code: -32000, message: err.message }
    });
  }
}

rl.on('line', async (line) => {
  try {
    const request = JSON.parse(line);

    switch (request.method) {
      case 'initialize':
        sendMessage({
          jsonrpc: '2.0',
          id: request.id,
          result: {
            protocolVersion: '2024-11-05',
            capabilities: { tools: {} },
            serverInfo: { name: 'music-theory-mcp', version: '1.0.0' }
          }
        });
        break;

      case 'tools/list':
        sendMessage({
          jsonrpc: '2.0',
          id: request.id,
          result: { tools: TOOLS }
        });
        break;

      case 'tools/call':
        await handleToolCall(request);
        break;

      default:
        sendMessage({
          jsonrpc: '2.0',
          id: request.id,
          result: { content: [] }
        });
    }
  } catch (err) {
    // Ignore malformed messages
  }
});

// Signal ready
console.error('MCP server started');
