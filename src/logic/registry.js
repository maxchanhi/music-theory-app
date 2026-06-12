const crypto = require('crypto');

const moduleRegistry = {};

const MODULE_PATHS = [
  '../logic/interval',
  '../logic/pitch_id',
  '../logic/chromatic',
  '../logic/clef_minor',
  '../logic/compound_simple',
  '../logic/duration_equation',
  '../logic/inversion',
  '../logic/melody_key',
  '../logic/transposing',
  '../logic/same_pitch',
  '../logic/instrument_knowledge'
];

function loadAll() {
  for (const modPath of MODULE_PATHS) {
    try {
      const mod = require(modPath);
      if (mod.meta && mod.generate && mod.check) {
        moduleRegistry[mod.meta.topic] = mod;
      }
    } catch (err) {
      console.warn(`Failed to load module ${modPath}:`, err.message);
    }
  }
}

function getModule(topic) {
  return moduleRegistry[topic] || null;
}

function listTopics() {
  return Object.keys(moduleRegistry).map(topic => ({
    topic,
    name: moduleRegistry[topic].meta.name,
    description: moduleRegistry[topic].meta.description,
    difficultyLevels: moduleRegistry[topic].meta.difficultyLevels,
    answerType: moduleRegistry[topic].meta.answerType
  }));
}

function generateQuestion(topic, options = {}) {
  const mod = getModule(topic);
  if (!mod) throw new Error(`Unknown topic: ${topic}`);
  const questionData = mod.generate(options);
  return {
    questionId: crypto.randomUUID(),
    topic,
    ...questionData
  };
}

function checkAnswer(topic, questionData, userAnswer) {
  const mod = getModule(topic);
  if (!mod) throw new Error(`Unknown topic: ${topic}`);
  const data = { ...questionData, ...(questionData.rawData || {}) };
  if (data.correctAnswer !== undefined && data.answer === undefined) {
    data.answer = data.correctAnswer;
  }
  if (data.answer === undefined) {
    return { correct: false, correctAnswer: 'unknown', explanation: 'Could not verify your answer. Please ask for a new question.' };
  }
  return mod.check(data, userAnswer);
}

loadAll();

module.exports = {
  getModule,
  listTopics,
  generateQuestion,
  checkAnswer,
  moduleRegistry
};
