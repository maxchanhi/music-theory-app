const express = require('express');
const router = express.Router();
const { generateQuestionData } = require('../logic/compound_simple');
const Feedback = require('../logic/feedback');

// GET /compound_simple
router.get('/', async (req, res) => {
    try {
        const questionData = generateQuestionData();
        
        // Store in session
        req.session.compoundSimpleData = {
            question: questionData.question,
            options: questionData.options,
            correctIndex: questionData.correctIndex
        };
        
        res.render('compound_simple', {
            vexData: questionData,
            question: questionData.question,
            submitted: false,
            user: req.session.user || null
        });
    } catch (err) {
        console.error('Error generating compound simple question:', err);
        res.status(500).send('Error generating question');
    }
});

// POST /compound_simple/generate (New Question)
router.post('/generate', (req, res) => {
    res.redirect('/compound_simple');
});

// POST /compound_simple/check
router.post('/check', async (req, res) => {
    try {
        const { optionIndex } = req.body;
        const sessionData = req.session.compoundSimpleData;
        
        if (!sessionData) {
            return res.redirect('/compound_simple');
        }
        
        const selectedOption = parseInt(optionIndex);
        const isCorrect = selectedOption === sessionData.correctIndex;
        
        // Save feedback if user is logged in
        if (req.session.user) {
            try {
                await Feedback.saveFeedback(
                    req.session.user._id,
                    'compound_simple',
                    isCorrect,
                    {
                        question: sessionData.question,
                        selectedOption: sessionData.options[selectedOption],
                        correctOption: sessionData.options[sessionData.correctIndex]
                    }
                );
            } catch (feedbackErr) {
                console.error('Error saving feedback:', feedbackErr);
            }
        }
        
        res.render('compound_simple', {
            vexData: sessionData,
            question: sessionData.question,
            submitted: true,
            selectedOption,
            correctIndex: sessionData.correctIndex,
            isCorrect,
            user: req.session.user || null
        });
        
    } catch (err) {
        console.error('Error checking answer:', err);
        res.status(500).send('Error checking answer');
    }
});

module.exports = router;
