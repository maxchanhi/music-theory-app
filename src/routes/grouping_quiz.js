const express = require('express');
const router = express.Router();
const groupingLogic = require('../logic/grouping_quiz');

// Simple in-memory session store (replace with express-session in production)
const sessions = {}; 

router.get('/', (req, res) => {
    // Basic session handling for demo purposes
    // In a real app, use express-session with proper IDs
    const sessionId = 'demo_user'; 
    
    if (!sessions[sessionId] || !sessions[sessionId].currentQuestion) {
        sessions[sessionId] = {
            currentQuestion: groupingLogic.getQuestion(),
            submitted: false,
            result: null
        };
    }

    const session = sessions[sessionId];
    
    const categoriesData = groupingLogic.categories.map(category => {
        let className = 'radio-label';
        let checked = false;
        let isCorrectAnswer = false;
        let isWrongAnswer = false;

        if (session.submitted && session.result) {
            className += ' result-dim';
            
            if (category === session.result.correctAnswer) {
                className += ' result-correct';
                isCorrectAnswer = true;
            } else if (category === session.result.userAnswer && !session.result.isCorrect) {
                className += ' result-wrong';
                isWrongAnswer = true;
            }
            
            if (category === session.result.userAnswer) {
                checked = true;
            }
        }

        return {
            name: category,
            className,
            checked,
            isCorrectAnswer,
            isWrongAnswer
        };
    });

    res.render('grouping_quiz', {
        question: session.currentQuestion,
        categories: groupingLogic.categories,
        categoriesData,
        submitted: session.submitted,
        result: session.result
    });
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const sessionId = 'demo_user';
    const session = sessions[sessionId];
    const { answer } = req.body;

    if (!session || !session.currentQuestion) {
        return res.redirect('/grouping_quiz');
    }

    const isCorrect = answer === session.currentQuestion.category;

    if (!isCorrect && req.session && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "grouping and beaming",
                details: `[('Wrong', 'User selected ${answer}, correct answer was ${session.currentQuestion.category}')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }
    
    session.submitted = true;
    session.result = {
        isCorrect: isCorrect,
        userAnswer: answer,
        correctAnswer: session.currentQuestion.category
    };

    res.redirect('/grouping_quiz');
});

router.post('/generate', (req, res) => {
    const sessionId = 'demo_user';
    sessions[sessionId] = {
        currentQuestion: groupingLogic.getQuestion(),
        submitted: false,
        result: null
    };
    res.redirect('/grouping_quiz');
});

module.exports = router;
