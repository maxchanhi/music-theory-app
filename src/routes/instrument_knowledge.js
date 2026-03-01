const express = require('express');
const router = express.Router();
const instrumentLogic = require('../logic/instrument_knowledge');

// In-memory session store (replace with proper session middleware in production)
const sessions = {};

router.get('/', (req, res) => {
    const sessionId = 'demo_user'; // For demo simplicity
    
    if (!sessions[sessionId]) {
        sessions[sessionId] = {
            currentQuestion: null,
            selectedTopics: instrumentLogic.topics, // Default to all
            submitted: false,
            result: null,
            history: [] // Store history for "AI feedback" placeholder
        };
    }
    
    const session = sessions[sessionId];
    
    // If no question exists, generate one
    if (!session.currentQuestion) {
        session.currentQuestion = instrumentLogic.getQuestion(session.selectedTopics);
    }

    res.render('instrument_knowledge', {
        question: session.currentQuestion,
        allTopics: instrumentLogic.topics,
        selectedTopics: session.selectedTopics,
        submitted: session.submitted,
        result: session.result,
        historyCount: session.history.length
    });
});

router.post('/generate', (req, res) => {
    const sessionId = 'demo_user';
    const session = sessions[sessionId];
    
    // Update selected topics if provided
    let { topics } = req.body;
    
    // Handle single checkbox selection (string) vs multiple (array) vs none
    if (topics) {
        if (!Array.isArray(topics)) {
            topics = [topics];
        }
        session.selectedTopics = topics;
    } else {
        // If no topics selected, keep previous or default? 
        // HTML form submission with unchecked checkboxes sends nothing.
        // We should probably enforce at least one topic or default to all if user unchecks all (or show error).
        // Let's default to all if empty to avoid crashes, or handle in UI.
        // Python code warns if no topic selected.
        // Here we'll just stick to previous selection if body is empty (might be a "Next Question" click without form data?)
        // Actually, the "Next Question" button might be outside the settings form.
    }

    // Generate new question
    session.currentQuestion = instrumentLogic.getQuestion(session.selectedTopics);
    session.submitted = false;
    session.result = null;
    
    res.redirect('/instrument_knowledge');
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const { answer } = req.body;
    const { currentQuestion } = req.session.instrument;
    
    if (!currentQuestion) return res.redirect('/instrument_knowledge');
    
    const correct = currentQuestion.answer;
    const isCorrect = answer === correct;
    
    if (!isCorrect && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "instrument knowledge",
                details: `[('Wrong', 'User selected ${answer}, correct answer was ${correct}')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }

    res.render('instrument_knowledge', {
        data: {
            question: currentQuestion,
            topics: req.session.instrument.selectedTopics
        },
        feedback: {
            correct: isCorrect,
            message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
        }
    });
});

router.post('/reset', (req, res) => {
    const sessionId = 'demo_user';
    if (sessions[sessionId]) {
        sessions[sessionId].history = [];
        sessions[sessionId].submitted = false;
        sessions[sessionId].result = null;
        sessions[sessionId].currentQuestion = null;
    }
    res.redirect('/instrument_knowledge');
});

module.exports = router;
