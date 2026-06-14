const express = require("express");
const session = require("express-session");
const MongoStore = require('connect-mongo').default || require('connect-mongo');
const path = require("path");
const connectDB = require('./config/database');
const authRouter = require('./routes/auth');
const chatRouter = require('./routes/chat');
const chromaticRouter = require('./routes/chromatic');
const clefMinorRouter = require('./routes/clef_minor');
const compoundSimpleRouter = require('./routes/compound_simple');
const durationEquationRouter = require('./routes/duration_equation');
const groupingQuizRouter = require('./routes/grouping_quiz');
const instrumentKnowledgeRouter = require('./routes/instrument_knowledge');
const intervalRouter = require('./routes/interval');
const inversionRouter = require('./routes/inversion');
const melodyKeyRouter = require('./routes/melody_key');
const pitchIdRouter = require('./routes/pitch_id');
const samePitchRouter = require('./routes/same_pitch');
const transposingRouter = require('./routes/transposing');
const pagesRouter = require('./routes/pages');
const tutorRouter = require('./routes/tutor');
const mcpTestRouter = require('./routes/mcp_test');

const createApp = () => {
  // Connect to Database
  connectDB();

  const app = express();
  const publicPath = path.join(__dirname, "..", "public");

  // Set up view engine
  app.set('view engine', 'ejs');
  app.set('views', path.join(__dirname, 'views'));
  
  // Explicitly require ejs to ensure it's bundled and available
  try {
    require('ejs');
  } catch (e) {
    console.error("EJS dependency check failed", e);
  }

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));
  app.use(express.static(publicPath));
  
  // Serve VexFlow from node_modules
  app.use('/scripts/vexflow', express.static(path.join(__dirname, '..', 'node_modules', 'vexflow', 'build', 'cjs')));
  
  // Session configuration
  app.use(session({
    secret: process.env.SESSION_SECRET || 'music-theory-secret-key',
    resave: false,
    saveUninitialized: false, // Changed to false for MongoStore optimization
    store: MongoStore.create({
      mongoUrl: process.env.MONGO_URI,
      collectionName: 'sessions',
      ttl: 24 * 60 * 60 // 1 day
    }),
    cookie: { 
      secure: process.env.NODE_ENV === 'production', 
      maxAge: 24 * 60 * 60 * 1000 // 1 day
    } 
  }));

  // Make user info available to all templates
  app.use((req, res, next) => {
    res.locals.user = req.session.userInfo || null;
    next();
  });
  
  app.get("/health", (req, res) => {
    res.status(200).json({ status: "ok" });
  });

  app.get("/", (req, res) => {
    res.render('index');
  });

  app.use('/', authRouter);
  app.use('/chat', chatRouter);
  app.use('/chromatic', chromaticRouter);
  app.use('/clef_minor', clefMinorRouter);
  app.use('/compound_simple', compoundSimpleRouter);
  app.use('/duration_equation', durationEquationRouter);
  app.use('/grouping_quiz', groupingQuizRouter);
  app.use('/instrument_knowledge', instrumentKnowledgeRouter);
  app.use('/interval', intervalRouter);
  app.use('/inversion', inversionRouter);
  app.use('/melody_key', melodyKeyRouter);
  app.use('/pitch_id', pitchIdRouter);
  app.use('/same_pitch', samePitchRouter);
  app.use('/transposing', transposingRouter);
  app.use('/', pagesRouter);
  app.use('/tutor', tutorRouter);
  app.use('/mcp', mcpTestRouter);

  return app;
};

module.exports = { createApp };
