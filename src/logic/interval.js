const noteLetters = ['c', 'd', 'e', 'f', 'g', 'a', 'b'];
const { clampMultiClef } = require('./ledger_utils');

// ── Accidental helpers ──────────────────────────────────────────
// Maps UI label → VexFlow accidental character
const accidentalLabelToVex = {
    'Sharp (♯)':        '#',
    'Natural (♮)':      '',
    'Flat (♭)':         'b',
    'Double-sharp(x)':  '##',
    'Double-flat(♭♭)':  'bb'
};

// Semitone offset from natural note
const accidentalOffset = { '': 0, '#': 1, 'b': -1, '##': 2, 'bb': -2 };

// Letter → semitone base (C=0, D=2, E=4, F=5, G=7, A=9, B=11)
const letterBase = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };

/** Compute absolute semitone from C0 for a VexFlow key like "c#/4". */
function keyToSemitone(key) {
    const m = key.match(/^([a-g])([#bn]*)\/(\d+)$/i);
    if (!m) return 0;
    const letter = m[1].toLowerCase();
    const acc = m[2] || '';
    const octave = parseInt(m[3], 10);
    // Normalize accidental: 'n' or '' → 0
    const cleanAcc = acc === 'n' ? '' : acc;
    return octave * 12 + (letterBase[letter] || 0) + (accidentalOffset[cleanAcc] || 0);
}

// ── Interval data ──────────────────────────────────────────────

const jumpChart = {
    "2,1":"Diminished","2,2":"Minor","2,3":"Major","2,4":"Augmented",
    "3,3":"Diminished","3,4":"Minor","3,5":"Major","3,6":"Augmented",
    "4,5":"Diminished","4,6":"Perfect","4,7":"Augmented",
    "5,7":"Diminished","5,8":"Perfect","5,9":"Augmented",
    "6,8":"Diminished","6,9":"Minor","6,10":"Major","6,11":"Augmented",
    "0,10":"Diminished","0,11":"Minor","0,12":"Major","0,13":"Augmented",
    "1,2":"Diminished","1,13":"Perfect","1,14":"Augmented",
    "1,1":"Perfect","1,12":"Augmented"
};

const numPlacement = {
    '1':"Unison",'2':"Second",'3':"Third",'4':"Fourth",'5':"Fifth",'6':"Sixth",'7':"Seventh",
    '8':"Octave",'9':"Ninth",'10':"Tenth",'11':"Eleventh",'12':"Twelfth",
    '13':"Thirteenth",'14':"Fourteenth",'15':"Compound Octave",
    '16':"Sixteenth",'17':"Seventeenth",'18':"Eighteenth",'19':"Nineteenth",
    '20':"Twentieth",'21':"Twenty-first",'22':"2 Compound Octaves",
    '23':"Twenty-third",'24':"Twenty-fourth",'25':"Twenty-fifth",
    '26':"Twenty-sixth",'27':"Twenty-seventh",'28':"Twenty-eighth",
    '29':"3 Compound Octaves"
};

const userIntervals = ["--","Unison","Second","Third","Fourth","Fifth","Sixth","Seventh",
    "Octave","Ninth","Tenth","Eleventh","Twelfth","Thirteenth","Fourteenth",
    "Compound Octave","Sixteenth","Seventeenth","Eighteenth","Nineteenth",
    "Twentieth","Twenty-first","2 Compound Octaves","Twenty-third","Twenty-fourth",
    "Twenty-fifth","Twenty-sixth","Twenty-seventh","Twenty-eighth","3 Compound Octaves"];

const userQualities = ["--","Diminished","Minor","Perfect","Major","Augmented"];

const difficultySettings = {
    "Beginner":          { clefs:["treble","bass"], sameClef:true, accs:['Natural (♮)'], compound:false },
    "Intermediate":      { clefs:["treble","bass"], sameClef:true, accs:['Flat (♭)','Natural (♮)','Sharp (♯)'], compound:false },
    "Advanced":          { clefs:["treble","bass"], sameClef:false, accs:['Flat (♭)','Natural (♮)','Sharp (♯)'], compound:true },
    "C clef Fanfare":    { clefs:["tenor","alto"], sameClef:true, accs:['Flat (♭)','Natural (♮)','Sharp (♯)'], compound:false },
    "Accidental Fanfare":{ clefs:["treble","bass"], sameClef:true, accs:['Flat (♭)','Natural (♮)','Sharp (♯)','Double-sharp(x)','Double-flat(♭♭)'], compound:true },
    "Expert":            { clefs:["treble","alto","tenor","bass"], sameClef:false, accs:['Flat (♭)','Natural (♮)','Sharp (♯)','Double-sharp(x)','Double-flat(♭♭)'], compound:true }
};

// ── Clef octave ranges (return octave number) ──────────────────
function clefOctave(clef) {
    const ranges = {
        treble: [4, 6],       // C4–C6
        alto:   [4, 6],
        tenor:  [4, 6],
        bass:   [3, 5]        // C3–C5
    };
    const opts = ranges[clef] || [4, 6];
    return opts[Math.floor(Math.random() * opts.length)];
}

// ── Interval calculation (takes octave numbers) ─────────────────
function calcInterval(oct1, oct2, pos1, pos2) {
    if (oct1 === oct2) {
        if (pos1 > pos2) return pos1 - pos2 + 1;
        if (pos1 < pos2) return pos2 - pos1 + 1;
        return 1;
    }
    if (oct1 > oct2) {
        return pos1 !== pos2 ? (pos1 - pos2) + ((oct1 - oct2) * 8) : (oct1 - oct2) * 8;
    }
    return pos1 !== pos2 ? pos2 - pos1 + ((oct2 - oct1) * 8) - 1 : (oct2 - oct1) * 8;
}

function calcSemitones(key1, key2) {
    const s1 = keyToSemitone(key1);
    const s2 = keyToSemitone(key2);
    const m1 = key1.match(/^([a-g])/i), m2 = key2.match(/^([a-g])/i);
    const l1 = m1 ? noteLetters.indexOf(m1[1].toLowerCase()) : 0;
    const l2 = m2 ? noteLetters.indexOf(m2[1].toLowerCase()) : 0;
    const o1 = parseInt((key1.match(/\/(\d+)/) || ['/4'])[1], 10);
    const o2 = parseInt((key2.match(/\/(\d+)/) || ['/4'])[1], 10);

    if (l1 === l2) {
        if (o1 < o2) return Math.abs(s2 - s1 - 1);
        if (o1 > o2) return Math.abs(s1 - s2 - 1);
        if (o1 === o2 && s1 !== s2) return 14;
    }
    if (s2 > s1) return s2 - s1 + 1;
    if (s2 < s1) return s2 + 13 - s1;
    return 1;
}

// ── Question generation ─────────────────────────────────────────

function generateQuestion(options = {}) {
    let settings = { ...difficultySettings[options.difficulty] || difficultySettings["Beginner"] };
    if (options.clefs) settings.clefs = options.clefs;
    if (options.accs) settings.accs = options.accs;
    if (options.sameClef !== undefined) settings.sameClef = options.sameClef;
    if (options.compound !== undefined) settings.compound = options.compound;
    const avoidKey = options.avoid; // e.g. "g/4-a/4" — skip this pair
    for (let attempt = 0; attempt < 10; attempt++) {
        const q = generateIntervalData(settings.clefs, settings.accs, settings.sameClef, settings.compound);
        if (!q) return null;
        const sig = (q.vexNote1?.key || '') + '-' + (q.vexNote2?.key || '');
        if (sig !== avoidKey) return q;
    }
    return generateIntervalData(settings.clefs, settings.accs, settings.sameClef, settings.compound);
}

function generateIntervalData(selectedClefs, selectedAccidentals, sameClef, compoundOctave) {
    if (!selectedClefs || selectedClefs.length === 0) selectedClefs = ["treble"];
    if (!selectedAccidentals || selectedAccidentals.length === 0) selectedAccidentals = ["Natural (♮)"];

    for (let loops = 0; loops < 200; loops++) {
        const clef1 = selectedClefs[Math.floor(Math.random() * selectedClefs.length)];
        const clef2 = sameClef ? clef1 : selectedClefs[Math.floor(Math.random() * selectedClefs.length)];

        const oct1 = clefOctave(clef1);
        const oct2 = compoundOctave ? clefOctave(clef2) : oct1;

        const accLabel1 = selectedAccidentals[Math.floor(Math.random() * selectedAccidentals.length)];
        const accLabel2 = selectedAccidentals[Math.floor(Math.random() * selectedAccidentals.length)];
        const acc1 = accidentalLabelToVex[accLabel1] || '';
        const acc2 = accidentalLabelToVex[accLabel2] || '';
        // For answer display: show natural as 'n', empty as ''
        const dispAcc1 = acc1 || 'n';
        const dispAcc2 = acc2 || 'n';

        const letter1 = noteLetters[Math.floor(Math.random() * noteLetters.length)];
        const letter2 = noteLetters[Math.floor(Math.random() * noteLetters.length)];

        // ── Original notes (for question text, answer, memory) ──
        const origKey1 = `${letter1}${acc1 === 'n' ? '' : acc1}/${oct1}`;
        const origKey2 = `${letter2}${acc2 === 'n' ? '' : acc2}/${oct2}`;

        // Skip identical notes 75% of the time
        if (origKey1 === origKey2 && Math.random() * 4 >= 1) continue;

        // ── Compute interval from ORIGINAL notes ──
        const pos1 = noteLetters.indexOf(letter1);
        const pos2 = noteLetters.indexOf(letter2);
        let intervalNum = calcInterval(oct1, oct2, pos1, pos2);
        const semitoneCount = calcSemitones(origKey1, origKey2);

        if (intervalNum >= 24) intervalNum -= 2;
        else if (intervalNum > 15 && intervalNum <= 23) intervalNum -= 1;

        const jKey = `${intervalNum % 7},${semitoneCount}`;
        if (!jumpChart[jKey]) continue;

        const quality = jumpChart[jKey];
        const numberName = numPlacement[intervalNum.toString()];
        const answer = `${quality} ${numberName}`;

        // ── Transposed VexFlow keys (for staff rendering only) ──
        // Each clef shifts notes so they sit nicely on its staff lines.
        // bass  +5 (up a 6th), tenor +1, alto -1 (one letter down)
        const clefShift = { bass: 5, tenor: 1, alto: -1 };
        let dispOct1 = oct1, dispOct2 = oct2;
        let dispLetter1 = letter1, dispLetter2 = letter2;

        const applyShift = (letter, oct, clef) => {
            const shift = clefShift[clef] || 0;
            if (!shift) return { letter, oct };
            const idx = noteLetters.indexOf(letter);
            let newIdx = idx + shift;
            let octDelta = 0;
            while (newIdx < 0) { newIdx += 7; octDelta--; }
            while (newIdx >= 7) { newIdx -= 7; octDelta++; }
            return {
                letter: noteLetters[newIdx],
                oct: oct + octDelta
            };
        };

        ({ letter: dispLetter1, oct: dispOct1 } = applyShift(letter1, oct1, clef1));
        ({ letter: dispLetter2, oct: dispOct2 } = applyShift(letter2, oct2, clef2));

        // Use natural key only — accidental is added via addModifier in the view
        const vn1 = { key: `${dispLetter1}/${dispOct1}`, accidental: dispAcc1 };
        const vn2 = { key: `${dispLetter2}/${dispOct2}`, accidental: dispAcc2 };

        // Clamp ledger lines on the transposed keys
        const clamped = clampMultiClef([
            { key: vn1.key, clef: clef1 },
            { key: vn2.key, clef: clef2 }
        ]);
        if (clamped[0].key !== vn1.key) { vn1.key = clamped[0].key; vn2.key = clamped[1].key; }

        // Note display name (from original letters, not transposed)
        const noteName = (letter, acc) => {
            if (!acc || acc === 'n') return letter;
            return letter + acc;
        };

        return {
            answer,
            quality,
            intervalName: numberName,
            clef1, clef2,
            note1: noteName(letter1, acc1 || ''),
            note2: noteName(letter2, acc2 || ''),
            vexNote1: vn1,
            vexNote2: vn2
        };
    }
    return null;
}

// ── Public API ──────────────────────────────────────────────────

function generate(options = {}) {
    const genOptions = { ...options };
    if (genOptions.clef && !genOptions.clefs) {
        genOptions.clefs = [genOptions.clef];
        genOptions.sameClef = true;
    }
    const q = generateQuestion(genOptions);
    if (!q) return null;

    const correctAnswer = `${q.quality} ${q.intervalName}`;

    return {
        questionText: `What is the interval between the two notes? (${q.note1} to ${q.note2})`,
        answerFormat: { type: 'composite', separator: ' ', fields: ['quality', 'interval'] },
        choices: {
            qualities: userQualities.filter(x => x !== '--'),
            intervals: userIntervals.filter(x => x !== '--')
        },
        correctAnswer,
        displayData: {
            vexNotes: [q.vexNote1, q.vexNote2],
            clefs: [q.clef1, q.clef2]
        },
        rawData: q
    };
}

function check(questionData, userAnswer) {
    const normalized = typeof userAnswer === 'string'
        ? userAnswer.trim()
        : `${userAnswer.quality || ''} ${userAnswer.interval || ''}`.trim();

    const correct = normalized.toLowerCase() === questionData.answer.toLowerCase();

    return {
        correct,
        correctAnswer: questionData.answer,
        explanation: correct
            ? 'Correct! You identified the interval accurately.'
            : `The correct answer is ${questionData.answer}. Remember to count the semitones between the two notes.`
    };
}

const meta = {
    topic: 'interval',
    name: 'Intervals',
    description: 'Identify the interval between two notes on a staff',
    difficultyLevels: Object.keys(difficultySettings),
    answerType: 'composite'
};

module.exports = {
    generateQuestion,
    generate,
    check,
    meta,
    userIntervals,
    userQualities,
    difficultySettings,
    accidentalNameMap: accidentalLabelToVex  // keep old export name for compatibility
};
