/**
 * Chat history memory — local file-based persistence.
 *
 * Each user gets a JSON file under .chat_history/{userId}.json.
 * Survives server restarts; no database required.
 */

const fs = require('fs');
const path = require('path');

const CHAT_DIR = path.resolve(__dirname, '..', '..', '.chat_history');
const MAX_HISTORY = 50; // keep last N messages per user

// Ensure the directory exists on first use
try { fs.mkdirSync(CHAT_DIR, { recursive: true }); } catch (_) {}

function filePath(userId) {
  // Sanitize: replace path separators and dots
  const safe = String(userId).replace(/[<>:"/\\|?*. ]/g, '_') || 'anonymous';
  return path.join(CHAT_DIR, `${safe}.json`);
}

/** Load a session from disk. Returns a fresh session if no file exists. */
function load(userId) {
  const fp = filePath(userId);
  try {
    const raw = fs.readFileSync(fp, 'utf8');
    const data = JSON.parse(raw);
    return {
      history: Array.isArray(data.history) ? data.history : [],
      state: data.state || 'IDLE',
      currentQuestionData: data.currentQuestionData || null,
      progress: data.progress || {
        level: 'beginner',
        weakAreas: [],
        strongAreas: [],
        totalQuestions: 0,
        correctCount: 0
      }
    };
  } catch (_) {
    // File missing or corrupted — return a fresh session
    return {
      history: [],
      state: 'IDLE',
      currentQuestionData: null,
      progress: {
        level: 'beginner',
        weakAreas: [],
        strongAreas: [],
        totalQuestions: 0,
        correctCount: 0
      }
    };
  }
}

/** Persist a session object to disk. */
function save(userId, session) {
  const fp = filePath(userId);
  // Cap history length
  if (session.history && session.history.length > MAX_HISTORY) {
    session.history = session.history.slice(-MAX_HISTORY);
  }
  const payload = JSON.stringify({
    history: session.history || [],
    state: session.state || 'IDLE',
    currentQuestionData: session.currentQuestionData || null,
    progress: session.progress || {
      level: 'beginner',
      weakAreas: [],
      strongAreas: [],
      totalQuestions: 0,
      correctCount: 0
    },
    updatedAt: new Date().toISOString()
  }, null, 2);
  fs.writeFileSync(fp, payload, 'utf8');
}

/** Append a single message to a user's history and persist. */
function appendMessage(userId, role, content) {
  const session = load(userId);
  session.history.push({ role, content, timestamp: new Date().toISOString() });
  save(userId, session);
  return session;
}

module.exports = { load, save, appendMessage };
