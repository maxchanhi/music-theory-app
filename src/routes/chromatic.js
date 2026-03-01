const express = require('express');
const router = express.Router();
const chromaticLogic = require('../logic/chromatic');
const chromaticGen = require('../logic/chromatic_generation');
const { Feedback } = require('../logic/feedback');

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

router.get('/', (req, res) => {
    // Initialize session data if not exists
    if (!req.session.chromatic) {
        req.session.chromatic = {
            chromaticScale: null,
            wrongOptions: null,
            ascending: null,
            files: [],
            selectedImage: null,
            clef: 'treble',
            vexFlowData: null,
            options: [] // To store shuffled options with their data
        };
    }

    res.render('chromatic', { 
        data: req.session.chromatic,
        message: null,
        messageType: null,
        feedback: null
    });
});

router.post('/generate', async (req, res) => {
    try {
        const clef = req.body.clef || 'treble';
        const ascending = Math.random() < 0.5;
        
        const chromaticScale = chromaticLogic.generateChromaticScale(ascending);
        const wrongOptions = chromaticLogic.generateWrongOptions(chromaticScale, ascending);
        
        // Generate VexFlow data instead of images
        const questionData = chromaticGen.generateQuestionData(
            chromaticScale, 
            wrongOptions, 
            ascending, 
            clef
        );
        
        // Prepare options for display
        // We need to mix correct and wrong answers but keep track of which is which
        const options = [];
        
        // Add correct option
        options.push({
            id: 'correct',
            notes: questionData.correct,
            isCorrect: true
        });
        
        // Add wrong options
        questionData.wrongs.forEach((wrongNotes, index) => {
            options.push({
                id: `wrong_${index}`,
                notes: wrongNotes,
                isCorrect: false
            });
        });
        
        shuffleArray(options);
        
        // Store in session
        req.session.chromatic = {
            chromaticScale,
            wrongOptions,
            ascending,
            clef,
            vexFlowData: questionData,
            options,
            selectedImage: null
        };
        
        res.redirect('/chromatic');
    } catch (err) {
        console.error(err);
        res.status(500).send("Error generating question");
    }
});

router.post('/select', (req, res) => {
    if (req.session.chromatic) {
        req.session.chromatic.selectedImage = req.body.image;
    }
    res.redirect('/chromatic');
});

router.post('/check', async (req, res) => {
    const { option } = req.body; // This will be the index or ID of the selected option
    const sessionData = req.session.chromatic;
    
    if (!sessionData) return res.redirect('/chromatic');
    
    // Find the selected option in the shuffled array
    const selectedOpt = sessionData.options.find(opt => opt.id === option);
    const isCorrect = selectedOpt && selectedOpt.isCorrect;
    
    if (!isCorrect && req.session.userInfo) {
        try {
            const feedback = new Feedback({
                user_id: req.session.userInfo.user_id,
                subject: "chromatic scale",
                details: `[('Wrong', 'User selected ${option}, correct answer was correct')]`
            });
            await feedback.save();
        } catch (err) {
            console.error("Error saving feedback:", err);
        }
    }

    res.render('chromatic', {
        data: sessionData,
        feedback: {
            correct: isCorrect,
            message: isCorrect ? 'Correct!' : 'Incorrect. Try again!'
        }
    });
});

module.exports = router;
