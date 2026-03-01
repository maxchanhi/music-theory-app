const express = require('express');
const router = express.Router();
const { generateDurationQuestion, generateTimeSignatureQuestion } = require('../logic/duration_equation');

// In-memory session storage (simplified for local use)
let sessionData = {
    duration: {
        question: null,
        submitted: false,
        isCorrect: false,
        userAnswer: '',
        correctAnswer: null,
        settings: {
            hard: false,
            simple: true,
            double_dotted: false
        }
    },
    timeSignature: {
        question: null,
        submitted: false,
        isCorrect: false,
        userAnswer: '',
        correctAnswer: null
    }
};

// Main page
router.get('/', (req, res) => {
    // If no questions exist, generate initial ones
    if (!sessionData.duration.question) {
        const q = generateDurationQuestion(sessionData.duration.settings);
        sessionData.duration.question = q.questionText;
        sessionData.duration.correctAnswer = q.correctAnswer;
    }
    
    if (!sessionData.timeSignature.question) {
        const q = generateTimeSignatureQuestion();
        sessionData.timeSignature.question = q.questionText;
        sessionData.timeSignature.correctAnswer = q.correctAnswer;
    }
    
    res.render('duration_equation', {
        duration: sessionData.duration,
        timeSignature: sessionData.timeSignature
    });
});

// Duration Quiz Routes
router.post('/duration/generate', (req, res) => {
    const { hard, simple, double_dotted } = req.body;
    
    // Update settings
    sessionData.duration.settings = {
        hard: hard === 'on',
        simple: simple === 'on',
        double_dotted: double_dotted === 'on'
    };
    
    // Generate new question
    const q = generateDurationQuestion(sessionData.duration.settings);
    sessionData.duration.question = q.questionText;
    sessionData.duration.correctAnswer = q.correctAnswer;
    sessionData.duration.submitted = false;
    sessionData.duration.userAnswer = '';
    sessionData.duration.isCorrect = false;
    
    res.redirect('/duration_equation');
});

const { Feedback } = require('../logic/feedback');

router.post('/duration/check', async (req, res) => {
    const { answer } = req.body;
    sessionData.duration.userAnswer = answer;
    sessionData.duration.submitted = true;
    
    // Check answer (allow string comparison)
    const isCorrect = answer.trim() === sessionData.duration.correctAnswer.toString();
    sessionData.duration.isCorrect = isCorrect;

    if (!isCorrect && req.session && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "duration equation",
                details: `[('Wrong', 'User selected ${answer}, correct answer was ${sessionData.duration.correctAnswer}')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }
    
    res.redirect('/duration_equation');
});

// Time Signature Quiz Routes
router.post('/time_signature/generate', (req, res) => {
    const q = generateTimeSignatureQuestion();
    sessionData.timeSignature.question = q.questionText;
    sessionData.timeSignature.correctAnswer = q.correctAnswer;
    sessionData.timeSignature.submitted = false;
    sessionData.timeSignature.userAnswer = '';
    sessionData.timeSignature.isCorrect = false;
    
    res.redirect('/duration_equation');
});

router.post('/time_signature/check', (req, res) => {
    const { answer } = req.body;
    sessionData.timeSignature.userAnswer = answer;
    sessionData.timeSignature.submitted = true;
    
    // Check answer
    sessionData.timeSignature.isCorrect = answer.trim() === sessionData.timeSignature.correctAnswer.toString();
    
    res.redirect('/duration_equation');
});

module.exports = router;
