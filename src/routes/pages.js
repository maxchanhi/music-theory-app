const express = require('express');
const router = express.Router();

router.get('/support_me', (req, res) => {
    res.render('support_me');
});

router.get('/about_me', (req, res) => {
    res.render('about_me');
});

module.exports = router;
