const express = require('express');
const router = express.Router();
const authLogic = require('../logic/auth');

// GET /login - Show login form
router.get('/login', (req, res) => {
    res.render('login', { error: null });
});

// POST /login - Handle login submission
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.render('login', { error: 'Please enter both username and password' });
    }

    const { isValid, userInfo } = await authLogic.verifyUser(username, password);

    if (isValid) {
        req.session.login = true;
        req.session.userInfo = userInfo;
        req.session.save(() => {
            res.redirect('/');
        });
    } else {
        res.render('login', { error: 'Invalid username or password' });
    }
});

// GET /logout - Logout user
router.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/login');
    });
});

module.exports = router;
