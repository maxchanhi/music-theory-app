const express = require('express');
const router = express.Router();
const path = require('path');
const { generateQuestionData, displayNote } = require('../logic/clef_minor');
const { generateQuestionImage } = require('../logic/clef_minor_generation');

// Simple in-memory session storage (not suitable for production with multiple users)
let sessionData = {
    currentQuestion: null,
    level: 'easy'
};

router.get('/', (req, res) => {
    res.render('clef_minor', { 
        question: sessionData.currentQuestion,
        level: sessionData.level,
        displayNote: displayNote,
        result: null
    });
});

router.post('/generate', async (req, res) => {
    try {
        const { level } = req.body;
        sessionData.level = level;
        
        const data = generateQuestionData(level);
        
        // Generate the image
        // In the Python code, it passes `minorScale` to `lilypond_score_uid`
        // My `generateQuestionData` returns `minorScale`
        
        await generateQuestionImage(data.clef, data.fixedPitch, data.minorScale);
        
        sessionData.currentQuestion = data;
        
        res.redirect('/clef_minor');
    } catch (error) {
        console.error("Error generating question:", error);
        res.status(500).send("Error generating question");
    }
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const { option } = req.body;
    const { question } = req.session.clefMinor;
    
    if (!question) return res.redirect('/clef_minor');
    
    const correct = question.answer;
    const isCorrect = option === correct;
    
    if (!isCorrect && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "clef and minor keys",
                details: `[('Wrong', 'User selected ${option}, correct answer was ${correct}')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }

    res.render('clef_minor', {
        data: question,
        feedback: {
            correct: isCorrect,
            message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
        }
    });
});

module.exports = router;
