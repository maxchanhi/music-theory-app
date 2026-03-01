const express = require('express');
const router = express.Router();
const { generateQuestionData: generateLogicData } = require('../logic/compound_simple');
const { generateQuestionData: generateVexData } = require('../logic/compound_simple_generation');
const { Feedback } = require('../logic/feedback');

router.get('/', async (req, res) => {
    // Initialize session data if not present
    if (!req.session.compoundSimple) {
        req.session.compoundSimple = {
            currentQuestion: null,
            vexData: null,
            submitted: false,
            selectedOption: null,
            isCorrect: false,
            correctIndex: -1
        };
    }

    if (!req.session.compoundSimple.currentQuestion) {
        const questionData = generateLogicData();
        const vexData = generateVexData(questionData);
        
        req.session.compoundSimple.currentQuestion = questionData;
        req.session.compoundSimple.vexData = vexData;
    }
    
    res.render('compound_simple', {
        question: req.session.compoundSimple.currentQuestion,
        vexData: req.session.compoundSimple.vexData,
        submitted: req.session.compoundSimple.submitted,
        selectedOption: req.session.compoundSimple.selectedOption,
        isCorrect: req.session.compoundSimple.isCorrect,
        correctIndex: req.session.compoundSimple.correctIndex
    });
});

router.post('/generate', async (req, res) => {
    try {
        if (!req.session.compoundSimple) {
            req.session.compoundSimple = {};
        }
        
        const questionData = generateLogicData();
        const vexData = generateVexData(questionData);
        
        req.session.compoundSimple.currentQuestion = questionData;
        req.session.compoundSimple.vexData = vexData;
        req.session.compoundSimple.submitted = false;
        req.session.compoundSimple.selectedOption = null;
        req.session.compoundSimple.isCorrect = false;
        req.session.compoundSimple.correctIndex = -1;
        
        res.redirect('/compound_simple');
    } catch (error) {
        console.error("Error generating question:", error);
        res.status(500).send("Error generating question");
    }
});

router.post('/check', async (req, res) => {
    const { optionIndex } = req.body;
    const idx = parseInt(optionIndex);
    
    if (req.session.compoundSimple && req.session.compoundSimple.currentQuestion && !isNaN(idx)) {
        req.session.compoundSimple.submitted = true;
        req.session.compoundSimple.selectedOption = idx;
        
        const questionData = req.session.compoundSimple.currentQuestion;
        const selectedOption = questionData.options[idx];
        const answer = questionData.answer;
        
        // Find correct index
        req.session.compoundSimple.correctIndex = questionData.options.findIndex(opt => 
            JSON.stringify(opt) === JSON.stringify(answer)
        );
        
        // Check if selected is correct
        const isCorrect = JSON.stringify(selectedOption) === JSON.stringify(answer);
        req.session.compoundSimple.isCorrect = isCorrect;

        // Save feedback if incorrect and user is logged in
        if (!isCorrect && req.session.userInfo) {
            try {
                // Construct details string matching the requested format:
                // "[('Correct', ''), ('Wrong', 'Reason...'), ...]"
                const detailsList = questionData.options.map(opt => {
                    if (opt.reason === "Correct") {
                        return "('Correct', '')";
                    } else {
                        // Escape single quotes in reason just in case
                        const reason = opt.reason.replace(/'/g, "\\'");
                        return `('Wrong', 'Reason for the wrong choice: ${reason}')`;
                    }
                });
                const detailsString = `[${detailsList.join(', ')}]`;

                const feedback = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "metric modulation",
                    details: detailsString
                });
                
                await feedback.save();
                console.log("Feedback saved for user:", req.session.userInfo.user_id);
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }
    }
    
    res.redirect('/compound_simple');
});

module.exports = router;
