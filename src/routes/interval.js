const express = require('express');
const router = express.Router();
const intervalLogic = require('../logic/interval');

// In-memory session store
const sessions = {};

router.get('/', (req, res) => {
    const sessionId = 'demo_user';
    
    if (!sessions[sessionId]) {
        sessions[sessionId] = {
            currentQuestion: null,
            settings: {
                difficulty: "Beginner",
                autoMode: true,
                clefs: ["treble"],
                accs: ["Natural (♮)"],
                sameClef: true,
                compound: false
            },
            feedback: null,
            lastAnswer: null
        };
    }
    
    const session = sessions[sessionId];
    
    if (!session.currentQuestion) {
        session.currentQuestion = intervalLogic.generateQuestion({
            difficulty: session.settings.difficulty
        });
        // Sync manual settings to current difficulty for display
        const diffSettings = intervalLogic.difficultySettings[session.settings.difficulty];
        if (session.settings.autoMode) {
            session.settings.clefs = diffSettings.clefs;
            session.settings.accs = diffSettings.accs;
            session.settings.sameClef = diffSettings.sameClef;
            session.settings.compound = diffSettings.compound;
        }
    }
    
    res.render('interval', {
        question: session.currentQuestion,
        settings: session.settings,
        feedback: session.feedback,
        lastAnswer: session.lastAnswer,
        userQualities: intervalLogic.userQualities,
        userIntervals: intervalLogic.userIntervals,
        difficulties: Object.keys(intervalLogic.difficultySettings),
        allClefs: ["treble", "bass", "alto", "tenor"],
        allAccs: Object.keys(intervalLogic.accidentalNameMap)
    });
});

router.post('/generate', (req, res) => {
    const sessionId = 'demo_user';
    const session = sessions[sessionId];
    
    const { difficulty, autoMode, clefs, accs, sameClef, compound } = req.body;
    
    // Update settings
    session.settings.difficulty = difficulty;
    session.settings.autoMode = (autoMode === 'on');
    
    if (!session.settings.autoMode) {
        // Manual settings
        session.settings.clefs = Array.isArray(clefs) ? clefs : (clefs ? [clefs] : ["treble"]);
        session.settings.accs = Array.isArray(accs) ? accs : (accs ? [accs] : ["Natural (♮)"]);
        session.settings.sameClef = (sameClef === 'on');
        session.settings.compound = (compound === 'on');
        
        session.currentQuestion = intervalLogic.generateQuestion({
            clefs: session.settings.clefs,
            accs: session.settings.accs,
            sameClef: session.settings.sameClef,
            compound: session.settings.compound
        });
    } else {
        // Auto mode
        session.currentQuestion = intervalLogic.generateQuestion({
            difficulty: session.settings.difficulty
        });
        // Update stored manual settings to match difficulty for UI consistency
        const diffSettings = intervalLogic.difficultySettings[session.settings.difficulty];
        session.settings.clefs = diffSettings.clefs;
        session.settings.accs = diffSettings.accs;
        session.settings.sameClef = diffSettings.sameClef;
        session.settings.compound = diffSettings.compound;
    }
    
    session.feedback = null;
    session.lastAnswer = null;
    
    res.redirect('/interval');
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const sessionId = 'demo_user';
    const session = sessions[sessionId];
    
    if (!session.currentQuestion) {
        return res.redirect('/interval');
    }
    
    const { quality, interval } = req.body;
    const userAnswer = `${quality} ${interval}`;
    const correct = session.currentQuestion.answer;
    
    session.lastAnswer = { quality, interval };
    
    if (userAnswer === correct) {
        session.feedback = {
            type: 'success',
            text: 'Correct! 🎉'
        };
    } else {
        session.feedback = {
            type: 'error',
            text: `Incorrect. The answer is ${correct}`
        };

        if (req.session && req.session.userInfo) {
            try {
                const feedback = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "interval quiz",
                    details: `[('Wrong', 'User selected ${userAnswer}, correct answer was ${correct}')]`
                });
                await feedback.save();
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }
    }
    
    res.redirect('/interval');
});

module.exports = router;
