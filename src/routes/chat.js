const express = require('express');
const OpenAI = require('openai');
const { getFeedbackByUserId } = require('../logic/feedback');
const router = express.Router();

// Initialize OpenAI client with DashScope configuration
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // Use the International endpoint (Singapore) as requested by user
    baseURL: process.env.DASHSCOPE_BASE_URL
});

// Middleware to check if user is logged in
const isAuthenticated = (req, res, next) => {
    if (req.session && req.session.login) {
        next();
    } else {
        res.redirect('/login');
    }
};

// GET route for the chat page
router.get('/', isAuthenticated, (req, res) => {
    res.render('chat', { 
        user: req.session.userInfo 
    });
});

// POST route for chat completions
router.post('/api/message', isAuthenticated, async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        // Fetch user feedback to use as context
        let feedbackContext = "";
        try {
            if (req.session.userInfo && req.session.userInfo.user_id) {
                const feedbackList = await getFeedbackByUserId(req.session.userInfo.user_id);
                if (feedbackList && feedbackList.length > 0) {
                    feedbackContext = "\n\nUser Feedback History (Use this to personalize your response):\n";
                    feedbackList.forEach((fb, index) => {
                        feedbackContext += `${index + 1}. Date: ${fb.date.toISOString().split('T')[0]}, Subject: ${fb.subject || 'General'}, Details: ${fb.details}\n`;
                    });
                }
            }
        } catch (err) {
            console.warn('Failed to fetch feedback context:', err);
        }

        const completion = await openai.chat.completions.create({
            model: process.env.LLM_MODEL || 'qwen-turbo',
            messages: [
                { role: 'system', content: `You are a helpful music theory assistant. You help students understand music theory concepts, analyze music, and answer questions about the app.${feedbackContext}` },
                { role: 'user', content: message }
            ],
        });

        res.json({ 
            reply: completion.choices[0].message.content 
        });
    } catch (error) {
        console.error('LLM API Error:', error);
        res.status(500).json({ 
            error: 'Failed to get response from AI assistant',
            details: error.message 
        });
    }
});

module.exports = router;