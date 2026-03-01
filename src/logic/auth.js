const mongoose = require('mongoose');

// Define User Schema to match legacy collection 'login'
// Note: Legacy code uses db['login']
const userSchema = new mongoose.Schema({
    user_name: {
        type: String,
        required: true
    },
    user_password: {
        type: String,
        required: true
    },
    // Include other fields as needed, based on usage in legacy app
    user_id: String,
    feedback_refs: [mongoose.Schema.Types.ObjectId]
}, { collection: 'login' }); // Explicitly set collection name

const User = mongoose.model('User', userSchema);

const verifyUser = async (username, password) => {
    try {
        const user = await User.findOne({ user_name: username, user_password: password });
        if (user) {
            return { isValid: true, userInfo: user };
        } else {
            return { isValid: false, userInfo: null };
        }
    } catch (error) {
        console.error(`verifyUser failed: ${error}`);
        return { isValid: false, userInfo: null };
    }
};

module.exports = {
    verifyUser,
    User
};
