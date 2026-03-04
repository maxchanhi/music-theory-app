const express = require('express');
const router = express.Router();
const clefMinorLogic = require('../logic/clef_minor');
const clefMinorGen = require('../logic/clef_minor_generation');
const { Feedback } = require('../logic/feedback');

router.get('/', (req, res) => {
    // Initialize session data if not exists
    if (!req.session.clefMinor) {
        req.session.clefMinor = {
            question: null,
            level: 'easy',
            vexFlowData: null
        };
    }

    // Get feedback from session (if exists) and clear it
    const feedback = req.session.clefMinorFeedback;
    delete req.session.clefMinorFeedback;

    console.log("GET /clef_minor - Session data:", {
        questionId: req.session.clefMinor?.question?.questionId,
        clef: req.session.clefMinor?.question?.clef,
        startingPitch: req.session.clefMinor?.question?.startingPitch,
        minorType: req.session.clefMinor?.question?.minorType,
        hasVexFlowData: !!req.session.clefMinor?.vexFlowData
    });

    // Set headers to prevent caching
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    res.set('Pragma', 'no-cache');
    res.set('Expires', '0');

    res.render('clef_minor', {
        data: req.session.clefMinor,
        feedback: feedback
    });
});

router.post('/generate', async (req, res) => {
    try {
        const { level } = req.body;

        // Generate question and check for duplicates
        let question;
        let attempts = 0;
        const maxAttempts = 10;
        
        // Get the previous question ID (if exists)
        const previousQuestionId = req.session.clefMinor?.question?.questionId || null;

        do {
            question = clefMinorLogic.generateQuestionData(level);
            attempts++;
            
            // Create a unique identifier for the question
            const questionId = `${question.clef}-${question.startingPitch}-${question.minorType}`;
            
            // Break if this is different from the previous question or max attempts reached
            // Skip duplicate check on first generation (previousQuestionId is null)
            if (previousQuestionId === null || questionId !== previousQuestionId || attempts >= maxAttempts) {
                break;
            }
        } while (attempts < maxAttempts);

        // Generate VexFlow data
        const vexFlowData = clefMinorGen.generateQuestionData(
            question.clef,
            question.fixedPitch,
            question.minorScale
        );

        // Store question ID for duplicate checking
        question.questionId = `${question.clef}-${question.startingPitch}-${question.minorType}`;

        console.log("Generated new question:", question.questionId);
        console.log("Previous question ID:", previousQuestionId);
        console.log("VexFlow notes:", vexFlowData.notes.slice(0, 3), '...');

        req.session.clefMinor = {
            question: question,
            level: level,
            vexFlowData: vexFlowData
        };

        // Save session before redirecting to ensure data persistence
        req.session.save((err) => {
            if (err) console.error("Session save error:", err);
            // Add timestamp to prevent browser caching
            res.redirect('/clef_minor?t=' + Date.now());
        });
    } catch (error) {
        console.error("Error generating question:", error);
        res.status(500).send("Error generating question");
    }
});

router.post('/check', async (req, res) => {
    console.log("Check answer request received", req.body);
    const { option } = req.body;
    const sessionData = req.session.clefMinor;

    if (!sessionData) {
        console.log("No session data found");
        return res.redirect('/clef_minor');
    }
    if (!sessionData.question) {
        console.log("No question in session data");
        return res.redirect('/clef_minor');
    }

    const question = sessionData.question;
    const correct = question.answer;

    console.log("User option:", option);
    console.log("Correct answer:", correct);

    // Safety check for undefined answer
    if (!correct) {
        console.error("Correct answer is undefined in session data:", question);
        // Force regeneration or show error
        return res.redirect('/clef_minor');
    }

    const isCorrect = option === correct;
    console.log("Is correct?", isCorrect);

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

    // Store feedback in session and redirect to prevent form resubmission
    req.session.clefMinorFeedback = {
        correct: isCorrect,
        message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
    };

    // Save session explicitly and redirect with timestamp to prevent caching
    req.session.save((err) => {
        if (err) {
            console.error("Session save error:", err);
        }
        res.redirect('/clef_minor?t=' + Date.now());
    });
});

module.exports = router;
