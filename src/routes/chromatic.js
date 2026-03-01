const express = require('express');
const router = express.Router();
const chromaticLogic = require('../logic/chromatic');
const chromaticGen = require('../logic/chromatic_generation');
const path = require('path');

// State management (per session in a real app, but here global for simplicity/demo)
// In a real production app, use express-session or similar.
let sessionData = {
    chromaticScale: null,
    wrongOptions: null,
    ascending: null,
    files: [],
    selectedImage: null,
    clef: 'treble'
};

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

router.get('/', (req, res) => {
    res.render('chromatic', { 
        data: sessionData,
        message: null,
        messageType: null
    });
});

router.post('/generate', async (req, res) => {
    try {
        const clef = req.body.clef || 'treble';
        sessionData.clef = clef;
        sessionData.ascending = Math.random() < 0.5;
        
        sessionData.chromaticScale = chromaticLogic.generateChromaticScale(sessionData.ascending);
        sessionData.wrongOptions = chromaticLogic.generateWrongOptions(sessionData.chromaticScale, sessionData.ascending);
        
        // Generate images
        await chromaticGen.generateQuestionImages(
            sessionData.chromaticScale, 
            sessionData.wrongOptions, 
            sessionData.ascending, 
            sessionData.clef
        );
        
        // Prepare file list for display
        sessionData.files = ["Correct.png"];
        for(let i=0; i<sessionData.wrongOptions.length; i++) {
            sessionData.files.push(`wrong_${i}.png`);
        }
        shuffleArray(sessionData.files);
        
        sessionData.selectedImage = null;
        
        res.redirect('/chromatic');
    } catch (err) {
        console.error(err);
        res.status(500).send("Error generating question");
    }
});

router.post('/select', (req, res) => {
    sessionData.selectedImage = req.body.image;
    res.redirect('/chromatic');
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const { option } = req.body;
    const { question } = req.session.chromatic;
    
    if (!question) return res.redirect('/chromatic');
    
    const correct = question.answer;
    const isCorrect = option === correct;
    
    if (!isCorrect && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "chromatic scale",
                details: `[('Wrong', 'User selected ${option}, correct answer was ${correct}')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }

    res.render('chromatic', {
        data: question,
        feedback: {
            correct: isCorrect,
            message: isCorrect ? 'Correct!' : `Incorrect. The correct answer was ${correct}.`
        }
    });
});

module.exports = router;
