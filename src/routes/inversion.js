const express = require('express');
const router = express.Router();
const { generateInversionQuestion, romanNumerial, inversionType, funEmojiList } = require('../logic/inversion');
const { Feedback } = require('../logic/feedback');

// In-memory storage for sessions (in a real app, use a database or Redis)
const sessions = {};

// Helper to get or create session
const getSession = (req) => {
    // For simplicity, we'll use a hardcoded session ID for this demo
    // In production, use express-session
    const sessionId = 'demo-session';
    if (!sessions[sessionId]) {
        sessions[sessionId] = {
            currentQuestion: null,
            clef: 'treble',
            feedback: null,
            lastAnswer: null
        };
    }
    return sessions[sessionId];
};

// GET /inversion - Show the quiz page
router.get('/', (req, res) => {
    const session = getSession(req);
    
    // Generate a question if none exists
    if (!session.currentQuestion) {
        session.currentQuestion = generateInversionQuestion(session.clef);
    }
    
    // Check if we have feedback stored in session (from a redirect or previous post)
    const feedback = session.feedback;
    const lastAnswer = session.lastAnswer;
    
    res.render('inversion', {
        question: session.currentQuestion,
        clef: session.clef,
        feedback: feedback,
        lastAnswer: lastAnswer,
        romanNumerial: romanNumerial,
        inversionType: inversionType
    });
    
    // Clear feedback after rendering, ONLY if it was a one-time thing?
    // Actually, in the Python version, feedback stays until new question.
    // So let's NOT clear it here.
});

// POST /inversion/generate - Generate a new question
router.post('/generate', (req, res) => {
    const session = getSession(req);
    const { clef } = req.body;
    
    if (clef) {
        session.clef = clef;
    }
    
    session.currentQuestion = generateInversionQuestion(session.clef);
    session.feedback = null;
    session.lastAnswer = null;
    
    res.redirect('/inversion');
});

// POST /inversion/check - Check the answer
router.post('/check', async (req, res) => {
    const session = getSession(req);
    const { numeral, inversion } = req.body;
    
    if (!session.currentQuestion) {
        return res.redirect('/inversion');
    }
    
    const userAnswer = `${numeral} ${inversion}`;
    const correctAnswer = session.currentQuestion.correctAnswer;
    
    const lastAnswer = { numeral, inversion };
    session.lastAnswer = lastAnswer;
    
    let feedback;
    if (userAnswer === correctAnswer) {
        const emo = funEmojiList[Math.floor(Math.random() * funEmojiList.length)];
        feedback = {
            type: 'success',
            text: `Correct! ${emo}`,
            isCorrect: true
        };
    } else {
        feedback = {
            type: 'error',
            text: `The correct answer is ${correctAnswer}`,
            isCorrect: false
        };

        if (req.session && req.session.userInfo) {
            try {
                const feedbackLog = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "inversion quiz",
                    details: `[('Wrong', 'User selected ${userAnswer}, correct answer was ${correctAnswer}')]`
                });
                await feedbackLog.save();
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }
    }
    session.feedback = feedback;
    
    // Render directly to show feedback immediately
    res.render('inversion', {
        question: session.currentQuestion,
        clef: session.clef,
        feedback: feedback,
        lastAnswer: lastAnswer,
        romanNumerial: romanNumerial,
        inversionType: inversionType
    });
});

module.exports = router;