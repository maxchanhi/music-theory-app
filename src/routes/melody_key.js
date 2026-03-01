
const express = require('express');
const router = express.Router();
const { 
    mainGeneration, 
    generateOptions, 
    mapToVexFlow, 
    keyscale, 
    easymode, 
    intermediate, 
    hard,
    funEmojiList 
} = require('../logic/melody_key');

// In-memory storage for sessions
const sessions = {};

const getSession = (req) => {
    const sessionId = 'demo-session'; // Simplified for demo
    if (!sessions[sessionId]) {
        sessions[sessionId] = {
            currentQuestion: null,
            difficulty: 'Easy',
            selectedKeys: [...easymode], // Default to easy mode keys
            feedback: null,
            lastAnswer: null
        };
    }
    return sessions[sessionId];
};

// GET /melody_key
router.get('/', (req, res) => {
    const session = getSession(req);
    
    // If no question, generate one
    if (!session.currentQuestion) {
        generateNewQuestion(session);
    }
    
    res.render('melody_key', {
        question: session.currentQuestion,
        difficulty: session.difficulty,
        feedback: session.feedback,
        lastAnswer: session.lastAnswer,
        allKeys: Object.keys(keyscale).sort(),
        difficulties: ['Easy', 'Intermediate', 'Advanced']
    });
});

// POST /melody_key/generate
router.post('/generate', (req, res) => {
    const session = getSession(req);
    const { difficulty } = req.body;
    
    if (difficulty) {
        session.difficulty = difficulty;
        // Update selected keys based on difficulty
        if (difficulty === 'Easy') session.selectedKeys = [...easymode];
        else if (difficulty === 'Intermediate') session.selectedKeys = [...intermediate];
        else if (difficulty === 'Advanced') session.selectedKeys = [...hard];
    }
    
    generateNewQuestion(session);
    session.feedback = null;
    session.lastAnswer = null;
    
    res.redirect('/melody_key');
});

const { Feedback } = require('../logic/feedback');

// POST /melody_key/check
router.post('/check', async (req, res) => {
    const session = getSession(req);
    const { answer } = req.body;
    
    if (!session.currentQuestion) {
        return res.redirect('/melody_key');
    }
    
    const isCorrect = answer === session.currentQuestion.correctAnswer;
    session.lastAnswer = answer;
    
    if (isCorrect) {
        const emoji = funEmojiList[Math.floor(Math.random() * funEmojiList.length)];
        session.feedback = {
            type: 'success',
            text: `Correct! ${emoji}`,
            isCorrect: true
        };
    } else {
        if (req.session && req.session.userInfo) {
            try {
                const feedback = new Feedback({
                    user_id: req.session.userInfo.user_id,
                    subject: "melody key",
                    details: `[('Wrong', 'User selected ${answer}, correct answer was ${session.currentQuestion.correctAnswer}')]`
                });
                await feedback.save();
            } catch (err) {
                console.error("Error saving feedback:", err);
            }
        }

        session.feedback = {
            type: 'error',
            text: `Incorrect. The correct answer is ${session.currentQuestion.correctAnswer}.`,
            isCorrect: false
        };
    }
    
    res.render('melody_key', {
        question: session.currentQuestion,
        difficulty: session.difficulty,
        feedback: session.feedback,
        lastAnswer: session.lastAnswer,
        allKeys: Object.keys(keyscale).sort(),
        difficulties: ['Easy', 'Intermediate', 'Advanced']
    });
});

function generateNewQuestion(session) {
    try {
        const keysPool = session.selectedKeys;
        if (!keysPool || keysPool.length === 0) {
            session.selectedKeys = [...easymode];
        }
        
        const ansKey = session.selectedKeys[Math.floor(Math.random() * session.selectedKeys.length)];
        let melody = mainGeneration(ansKey);
        
        if (!melody || melody.length === 0) {
            console.error('Failed to generate melody for key:', ansKey);
            // Fallback to a simple C major scale if generation fails completely
            const cMajor = keyscale["C major"];
            melody = cMajor.slice(0, 4).map(p => [p, "4"]);
        }

        console.log('Generated melody for key:', ansKey);
        // console.log('Melody:', JSON.stringify(melody)); // Reduce log noise

        const options = generateOptions(ansKey, session.selectedKeys);
        const vexFlowNotes = mapToVexFlow(melody);
        
        // Create Tone.js friendly notes format
        const toneNotes = melody.map(note => {
            let pitch = note[0];
            // Convert 's' to '#', 'f' to 'b'
            if (pitch.endsWith('ss')) pitch = pitch.slice(0, -2) + '##'; 
            else if (pitch.endsWith('s')) pitch = pitch.slice(0, -1) + '#';
            else if (pitch.length > 1 && pitch.endsWith('f')) pitch = pitch.slice(0, -1) + 'b';
            
            // Uppercase pitch letter
            pitch = pitch.charAt(0).toUpperCase() + pitch.slice(1);
            
            // Add octave (default 4)
            pitch = pitch + '4';
            
            let duration = note[1];
            let toneDur = duration;
            if (duration === '2') toneDur = '2n';
            else if (duration === '4') toneDur = '4n';
            else if (duration === '8') toneDur = '8n';
            else if (duration === '16') toneDur = '16n';
            else if (duration === '4.') toneDur = '4n.';
            else if (duration === '8.') toneDur = '8n.';
            
            return { pitch, duration: toneDur };
        });

        session.currentQuestion = {
            correctAnswer: ansKey,
            options: options,
            vexFlowNotes: vexFlowNotes,
            toneNotes: toneNotes
        };
    } catch (err) {
        console.error("Error in generateNewQuestion:", err);
        // Ensure session has a valid question even if error, to avoid crashing view
        session.currentQuestion = null; 
    }
}

module.exports = router;
