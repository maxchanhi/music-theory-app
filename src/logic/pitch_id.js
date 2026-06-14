const note_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
const { clampLedgerLines } = require('./ledger_utils');

const accidentalsMap = {
    'Flat (♭)': 'b',
    'Natural (♮)': 'n',
    'Sharp (♯)': '#',
    'Double-sharp (x)': '##',
    'Double-flat (𝄫)': 'bb',
    // MCP param versions (no space before paren)
    'Double-sharp(x)': '##',
    'Double-flat(♭♭)': 'bb',
};

const accidentalsList = Object.keys(accidentalsMap);

const levels = {
    "basic":         { clefs:["treble","bass"], accidentals:['Natural (♮)'] },
    "intermediate":  { clefs:["treble","bass"], accidentals:['Flat (♭)','Natural (♮)','Sharp (♯)'] },
    "advanced":      { clefs:["treble","bass"], accidentals:accidentalsList },
    "c clefs":       { clefs:["alto","tenor"],  accidentals:['Natural (♮)'] },
    "all clefs":     { clefs:["treble","alto","tenor","bass"], accidentals:accidentalsList }
};

// ── Note pools in VexFlow key format (letter/octave) ────────────
const clefsData = {
    treble: {
        instaff:     ['d/4','e/4','f/4','g/4','a/4','b/4','c/5','d/5','e/5','f/5','g/5'],
        leger_lines: ['g/3','a/3','b/3','c/4','a/5','b/5','c/6','d/6']
    },
    bass: {
        instaff:     ['f/2','g/2','a/2','b/2','c/3','d/3','e/3','f/3','g/3','a/3','b/3'],
        leger_lines: ['c/2','d/2','e/2','c/4','d/4','e/4','f/4']
    },
    tenor: {
        instaff:     ['c/4','d/4','e/4','f/4','g/4','a/4','b/4','c/5','d/5','e/5','f/5'],
        leger_lines: ['g/3','a/3','b/3','g/5','a/5','b/5','c/6']
    },
    alto: {
        instaff:     ['e/4','f/4','g/4','a/4','b/4','c/5','d/5','e/5','f/5','g/5','a/5'],
        leger_lines: ['c/4','d/4','b/5','c/6','d/6','e/6']
    }
};

// ── Question generation ─────────────────────────────────────────

function generateQuestion(options) {
    const avoidKey = options.avoid; // skip this vexKey
    for (let attempt = 0; attempt < 10; attempt++) {
        const q = generateQuestionInner(options);
        if (!q) return q;
        if (q.vexKey !== avoidKey) return q;
    }
    return generateQuestionInner(options);
}

function generateQuestionInner(options) {
    // Accept MCP param names as aliases
    let poolClefs = options.clefs || options.selectedClefs;
    let poolAccidentals = options.accs || options.selectedAccidentals;

    // Map difficulty preset if provided (overrides explicit clefs/accidentals)
    if (options.difficulty) {
      const preset = levels[options.difficulty.toLowerCase().replace(/\s+/g, '_')]
                  || levels[options.difficulty]
                  || levels[Object.keys(levels).find(k => k.replace(/_/g, ' ') === options.difficulty.toLowerCase())];
      if (preset) {
        poolClefs = preset.clefs;
        poolAccidentals = preset.accidentals;
      }
    }

    if (!poolClefs || poolClefs.length === 0) poolClefs = ["treble"];
    if (!poolAccidentals || poolAccidentals.length === 0) poolAccidentals = ['Natural (♮)'];

    const chosenClef = poolClefs[Math.floor(Math.random() * poolClefs.length)];
    const clefInfo = clefsData[chosenClef] || clefsData.treble;

    const chosenAccidentalLabel = poolAccidentals[Math.floor(Math.random() * poolAccidentals.length)];
    const vexAccidental = accidentalsMap[chosenAccidentalLabel] || 'n';

    const noteList = options.useLedger ? clefInfo.leger_lines : clefInfo.instaff;
    const validNoteList = (noteList && noteList.length > 0) ? noteList : clefInfo.instaff;

    // Already a VexFlow key, e.g. "c/4"
    const chosenKey = validNoteList[Math.floor(Math.random() * validNoteList.length)];

    // Clamp ledger lines
    const clampedKey = clampLedgerLines(chosenClef, [chosenKey])[0];

    // Extract note letter for answer (e.g. "c" from "c/4")
    const noteLetter = (clampedKey.match(/^([a-g])/i) || ['?'])[1].toUpperCase();

    return {
        clef: chosenClef,
        vexKey: clampedKey,
        accidental: vexAccidental,
        answer: {
            note: noteLetter,
            accidental: chosenAccidentalLabel
        }
    };
}

function generate(options = {}) {
    const q = generateQuestion(options);
    return {
        questionText: `Identify the note. What note is this?`,
        answerFormat: { type: 'composite', separator: ' ', fields: ['note', 'accidental'] },
        choices: null,
        correctAnswer: `${q.answer.note} ${q.answer.accidental}`,
        displayData: {
            clef: q.clef,
            vexKey: q.vexKey,
            accidental: q.accidental
        },
        rawData: q
    };
}

function check(questionData, userAnswer) {
    let userNote, userAcc;
    if (typeof userAnswer === 'string') {
        const raw = userAnswer.trim();
        // Support single-word format: "fbb" (letter + accidental suffix)
        const m = raw.match(/^([a-gA-G])([#bnx]{1,2}|bb|##|xx|double.?flat|double.?sharp|flat|sharp|natural)?$/i);
        if (m) {
            userNote = m[1].toUpperCase();
            const suffix = (m[2] || '').toLowerCase();
            const suffixMap = {
                '': 'Natural (♮)', 'n': 'Natural (♮)', 'natural': 'Natural (♮)',
                '#': 'Sharp (♯)', 'sharp': 'Sharp (♯)', 's': 'Sharp (♯)',
                'b': 'Flat (♭)', 'flat': 'Flat (♭)', 'f': 'Flat (♭)',
                '##': 'Double-sharp(x)', 'xx': 'Double-sharp(x)', 'x': 'Double-sharp(x)', 'doublesharp': 'Double-sharp(x)',
                'bb': 'Double-flat(♭♭)', 'doubleflat': 'Double-flat(♭♭)',
            };
            userAcc = suffixMap[suffix] || 'Natural (♮)';
        } else {
            const parts = raw.split(/\s+/);
            userNote = parts[0] || '';
            userAcc = parts.slice(1).join(' ') || 'Natural (♮)';
        }
    } else {
        userNote = userAnswer.note || '';
        userAcc = userAnswer.accidental || 'Natural (♮)';
    }

    // Normalize accidental label for comparison (e.g. "bb" → "Double-flat(♭♭)")
    const accLabelMap = {
        'natural (♮)': 'Natural (♮)', 'natural': 'Natural (♮)', 'n': 'Natural (♮)',
        'flat (♭)': 'Flat (♭)', 'flat': 'Flat (♭)', 'b': 'Flat (♭)',
        'sharp (♯)': 'Sharp (♯)', 'sharp': 'Sharp (♯)', '#': 'Sharp (♯)',
        'double-sharp(x)': 'Double-sharp(x)', 'double-sharp': 'Double-sharp(x)', '##': 'Double-sharp(x)', 'x': 'Double-sharp(x)', 'xx': 'Double-sharp(x)',
        'double-flat(♭♭)': 'Double-flat(♭♭)', 'double-flat': 'Double-flat(♭♭)', 'bb': 'Double-flat(♭♭)',
    };
    const correctNote = userNote.toUpperCase() === questionData.answer.note.toUpperCase();
    const normalizedAcc = accLabelMap[userAcc.trim().toLowerCase()] || userAcc.trim();
    const correctAcc = normalizedAcc === questionData.answer.accidental;
    const correct = correctNote && correctAcc;

    return {
        correct,
        correctAnswer: `${questionData.answer.note} ${questionData.answer.accidental}`,
        explanation: correct
            ? 'Correct! You identified the note accurately.'
            : `The correct answer is ${questionData.answer.note} ${questionData.answer.accidental}. Pay attention to the clef and accidental.`
    };
}

const meta = {
    topic: 'pitch_id',
    name: 'Pitch Identification',
    description: 'Identify note names and accidentals across different clefs',
    difficultyLevels: Object.keys(levels),
    answerType: 'composite'
};

module.exports = {
    generateQuestion,
    generate,
    check,
    meta,
    levels,
    note_letters,
    accidentalsList
};
