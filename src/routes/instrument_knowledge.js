const express = require('express');
const router = express.Router();
const instrumentLogic = require('../logic/instrument_knowledge');
const { Feedback } = require('../logic/feedback');

router.get('/', (req, res) => {
    // Initialize session if not exists
    if (!req.session.instrument) {
        req.session.instrument = {
            currentQuestion: null,
            selectedTopics: instrumentLogic.topics, // Default to all
            submitted: false,
            result: null,
            history: [] // Store history for "AI feedback" placeholder
        };
    }
    
    const session = req.session.instrument;
    
    // If no question exists, generate one
    if (!session.currentQuestion) {
        session.currentQuestion = instrumentLogic.getQuestion(session.selectedTopics);
    }

    // Check for feedback from redirect (if any)
    const feedback = req.session.instrumentFeedback;
    delete req.session.instrumentFeedback;

    res.render('instrument_knowledge', {
        question: session.currentQuestion,
        allTopics: instrumentLogic.topics,
        selectedTopics: session.selectedTopics,
        submitted: session.submitted,
        result: session.result,
        historyCount: session.history ? session.history.length : 0,
        feedback: feedback
    });
});

router.post('/generate', (req, res) => {
    // Ensure session exists
    if (!req.session.instrument) {
        req.session.instrument = {
            currentQuestion: null,
            selectedTopics: instrumentLogic.topics,
            submitted: false,
            result: null,
            history: []
        };
    }

    const session = req.session.instrument;
    
    // Update selected topics if provided
    let { topics } = req.body;
    
    // Handle single checkbox selection (string) vs multiple (array) vs none
    if (topics) {
        if (!Array.isArray(topics)) {
            topics = [topics];
        }
        session.selectedTopics = topics;
    } else {
        // If no topics selected (empty form submission), maybe keep previous or default to all?
        // If the user unchecked everything, we should probably enforce at least one or reset to all.
        // For now, let's keep the previous selection if topics is undefined, 
        // but HTML forms send nothing if no checkbox is checked.
        // To handle "uncheck all", we might need a hidden input or assume empty means empty.
        // But the logic might fail with empty topics.
        // Let's default to all if nothing is selected to be safe.
        if (req.body.topics === undefined) { 
             // If the form was submitted but no topics were checked (and we assume form was submitted)
             // We can check if this is a "generate" action from the settings form.
             // But simpler to just ensure we have some topics.
             // If we want to persist "no change" when just clicking "Next Question", we need to know where the request came from.
             // Assuming the form includes the current selection.
        }
    }

    // Generate new question
    session.currentQuestion = instrumentLogic.getQuestion(session.selectedTopics);
    session.submitted = false;
    session.result = null;
    
    req.session.save((err) => {
        if (err) console.error("Session save error:", err);
        res.redirect('/instrument_knowledge');
    });
});

router.post('/check', async (req, res) => {
    // Ensure session exists
    if (!req.session.instrument) {
        return res.redirect('/instrument_knowledge');
    }

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

    // Store feedback in session and redirect
    req.session.instrumentFeedback = {
        correct: isCorrect,
        message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
    };
    
    // Update session state if needed (e.g. mark as submitted)
    req.session.instrument.submitted = true;
    req.session.instrument.result = {
        isCorrect: isCorrect,
        correctAnswer: correct,
        userAnswer: answer
    };

    req.session.save((err) => {
        if (err) console.error("Session save error:", err);
        res.redirect('/instrument_knowledge');
    });
});

module.exports = router;
