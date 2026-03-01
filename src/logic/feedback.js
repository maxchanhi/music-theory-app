const mongoose = require('mongoose');

// Define Feedback Schema
const feedbackSchema = new mongoose.Schema({
    user_id: {
        type: String,
        required: true
    },
    date: {
        type: Date,
        default: Date.now
    },
    subject: String,
    details: String
}, { collection: 'feedback' });

const Feedback = mongoose.model('Feedback', feedbackSchema);

const getFeedbackByUserId = async (userId) => {
    try {
        // Handle user_ prefix stripping if needed (legacy compatibility)
        let normalizedUserId = userId;
        if (userId.startsWith('user_')) {
            normalizedUserId = userId.substring(5);
        }

        // Try both with and without prefix just in case
        const feedback = await Feedback.find({
            $or: [
                { user_id: normalizedUserId },
                { user_id: userId }
            ]
        }).sort({ date: -1 }).limit(10); // Get last 10 entries

        return feedback;
    } catch (error) {
        console.error(`getFeedbackByUserId failed: ${error}`);
        return [];
    }
};

module.exports = {
    Feedback,
    getFeedbackByUserId
};
