const express = require('express');
const router = express.Router();
const pitchLogic = require('../logic/pitch_id');

// Middleware to ensure session structure
router.use((req, res, next) => {
    if (!req.session.pitch_id) {
        req.session.pitch_id = {
            difficulty: 'basic',
            useLedger: false,
            selectedClefs: pitchLogic.levels['basic'].clefs,
            selectedAccidentals: pitchLogic.levels['basic'].accidentals,
            currentQuestion: null
        };
    }
    next();
});

router.get('/', (req, res) => {
    // Generate new question
    const question = pitchLogic.generateQuestion({
        difficulty: req.session.pitch_id.difficulty,
        useLedger: req.session.pitch_id.useLedger,
        selectedClefs: req.session.pitch_id.selectedClefs,
        selectedAccidentals: req.session.pitch_id.selectedAccidentals
    });
    
    req.session.pitch_id.currentQuestion = question;
    
    res.render('pitch_id', {
        question: question,
        settings: req.session.pitch_id,
        levels: Object.keys(pitchLogic.levels),
        noteLetters: pitchLogic.note_letters,
        accidentalsList: pitchLogic.accidentalsList,
        feedback: null
    });
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const { note, accidental } = req.body;
    const currentQ = req.session.pitch_id.currentQuestion;
    
    if (!currentQ) {
        return res.redirect('/pitch_id');
    }
    
    const isCorrect = (note === currentQ.answer.note && accidental === currentQ.answer.accidental);

    if (!isCorrect && req.session.userInfo) {
        try {
            const feedbackLog = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "pitch identification",
                details: `[('Wrong', 'User selected ${note} ${accidental}, correct answer was ${currentQ.answer.note} ${currentQ.answer.accidental}')]`
            });
            await feedbackLog.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }
    
    const feedback = {
        isCorrect: isCorrect,
        correctAnswer: `${currentQ.answer.note} ${currentQ.answer.accidental}`,
        userAnswer: `${note} ${accidental}`,
        text: isCorrect ? "Correct! 🎉" : `Incorrect. The answer was ${currentQ.answer.note} ${currentQ.answer.accidental}`,
        type: isCorrect ? "success" : "error"
    };
    
    res.render('pitch_id', {
        question: currentQ,
        settings: req.session.pitch_id,
        levels: Object.keys(pitchLogic.levels),
        noteLetters: pitchLogic.note_letters,
        accidentalsList: pitchLogic.accidentalsList,
        feedback: feedback,
        lastAnswer: { note, accidental }
    });
});

router.post('/settings', (req, res) => {
    const { difficulty, useLedger } = req.body;
    
    if (difficulty && pitchLogic.levels[difficulty]) {
        req.session.pitch_id.difficulty = difficulty;
        req.session.pitch_id.selectedClefs = pitchLogic.levels[difficulty].clefs;
        req.session.pitch_id.selectedAccidentals = pitchLogic.levels[difficulty].accidentals;
    }
    
    req.session.pitch_id.useLedger = (useLedger === 'on');
    
    res.redirect('/pitch_id');
});

module.exports = router;
