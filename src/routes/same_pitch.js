const express = require('express');
const router = express.Router();
const samePitchLogic = require('../logic/same_pitch');

// Middleware to initialize session if needed
router.use((req, res, next) => {
    if (!req.session.same_pitch) {
        req.session.same_pitch = {
            currentQuestion: null
        };
    }
    next();
});

router.get('/', (req, res) => {
    const question = samePitchLogic.generateQuestion();
    req.session.same_pitch.currentQuestion = question;
    
    res.render('same_pitch', {
        question: question,
        feedback: null,
        selectedIndices: []
    });
});

const { Feedback } = require('../logic/feedback');

router.post('/check', async (req, res) => {
    const { selectedIndices } = req.body; // Expecting array of strings/numbers like ['0', '2']
    const question = req.session.same_pitch.currentQuestion;
    
    if (!question || !selectedIndices || !Array.isArray(selectedIndices)) {
        return res.redirect('/same_pitch');
    }
    
    // Convert to integers
    const indices = selectedIndices.map(i => parseInt(i, 10));
    
    // Check if exactly 2 are selected
    if (indices.length !== 2) {
        return res.render('same_pitch', {
            question: question,
            feedback: { type: 'error', text: 'Please select exactly two options.' },
            selectedIndices: indices
        });
    }
    
    // Verify answer
    // The options with type 'same' are the correct ones.
    const correctIndices = question.options
        .map((opt, index) => opt.type === 'same' ? index : -1)
        .filter(index => index !== -1);
        
    // Check if user selected indices match correct indices
    const isCorrect = indices.every(i => correctIndices.includes(i)) && indices.length === correctIndices.length;
    
    let feedback;
    if (isCorrect) {
        feedback = { type: 'success', text: 'Correct! Both melodies sound the same.' };
    } else {
        feedback = { 
            type: 'error', 
            text: `Incorrect. The correct options were ${correctIndices.map(i => i + 1).join(' and ')}.` 
        };

        if (req.session.userInfo) {
            try {
                const feedbackLog = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "same pitch",
                    details: `[('Wrong', 'User selected options ${indices.map(i => i + 1).join(', ')}, correct options were ${correctIndices.map(i => i + 1).join(', ')}') ]`
                });
                await feedbackLog.save();
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }
    }
    
    res.render('same_pitch', {
        question: question,
        feedback: feedback,
        selectedIndices: indices,
        correctIndices: correctIndices
    });
});

module.exports = router;
