const serverless = require('serverless-http');
const { createApp } = require('../../src/app');

// Initialize app outside handler to reuse warm instances
const app = createApp();

module.exports.handler = serverless(app);
