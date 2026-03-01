const express = require('express');
const router = express.Router();
const transposingLogic = require('../logic/transposing');

// Middleware to ensure session is initialized
router.use((req, res, next) => {
    if (!req.session.transposing) {
        req.session.transposing = {
            currentQuestion: null,
            correctCount: 0,
            totalCount: 0
        };
    }
    next();
});

// GET route to render the quiz
router.get('/', (req, res) => {
    // Generate a new question if one doesn't exist or if requested
    if (!req.session.transposing.currentQuestion || req.query.new === 'true') {
        try {
            const question = transposingLogic.generateQuestion();
            req.session.transposing.currentQuestion = question;
        } catch (error) {
            console.error("Error generating transposition question:", error);
            return res.status(500).send("Error generating question");
        }
    }
    
    const question = req.session.transposing.currentQuestion;
    
    res.render('transposing', {
        question: question,
        feedback: null,
        selectedOption: null
    });
});

const { Feedback } = require('../logic/feedback');

// POST route to check answer
router.post('/check', async (req, res) => {
    const { selectedOption } = req.body;
    const question = req.session.transposing.currentQuestion;
    
    if (!question) {
        return res.redirect('/transposing');
    }
    
    const selectedIdx = parseInt(selectedOption);
    const correctOption = question.options.find(opt => opt.type === 'correct');
    const isCorrect = question.options[selectedIdx].type === 'correct';
    
    if (isCorrect) {
        req.session.transposing.correctCount++;
    } else {
        if (req.session.userInfo) {
            try {
                const feedbackLog = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "transposition quiz",
                    details: `[('Wrong', 'User selected option ${selectedIdx + 1}, correct answer was option ${question.options.indexOf(correctOption) + 1}')]`
                });
                await feedbackLog.save();
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }
    }
    req.session.transposing.totalCount++;
    
    res.render('transposing', {
        question: question,
        feedback: isCorrect ? 'Correct!' : `Incorrect. The correct answer was Option ${question.options.indexOf(correctOption) + 1}`,
        selectedOption: selectedIdx,
        isCorrect: isCorrect
    });
});

module.exports = router;
