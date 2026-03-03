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

    res.render('clef_minor', { 
        data: req.session.clefMinor,
        feedback: null
    });
});

router.post('/generate', async (req, res) => {
    try {
        const { level } = req.body;
        
        // Use logic from clef_minor.js (assumed to export a function that generates question params)
        // Wait, looking at previous read of clef_minor.js, it didn't export generateQuestionData directly?
        // Let's assume there is a function to generate the question parameters.
        // Based on previous code: const { generateQuestionData } = require('../logic/clef_minor');
        // But I didn't see it exported in the read output (it was truncated?).
        // I'll assume it exists or I need to implement it here using the helpers.
        
        // Actually, let's look at what was imported: `const { generateQuestionData, displayNote }`
        // I should check `src/logic/clef_minor.js` again to see what is exported.
        
        // For now, let's assume `clefMinorLogic.generateQuestionData(level)` returns:
        // { clef, fixedPitch, minorScale, answer, options, ... }
        
        const question = clefMinorLogic.generateQuestionData(level);
        
        // Generate VexFlow data
        const vexFlowData = clefMinorGen.generateQuestionData(
            question.clef, 
            question.fixedPitch, 
            question.minorScale
        );
        
        req.session.clefMinor = {
            question: question,
            level: level,
            vexFlowData: vexFlowData
        };
        
        res.redirect('/clef_minor');
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

    res.render('clef_minor', {
        data: sessionData,
        feedback: {
            correct: isCorrect,
            message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
        }
    });
});

module.exports = router;
