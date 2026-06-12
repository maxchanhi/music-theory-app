const noteLetters = ['c', 'd', 'e', 'f', 'g', 'a', 'b'];

// Maps Python's accidentals_lilypond keys to suffixes
const accidentalNameMap = {
    'Sharp (♯)': 'is',
    'Natural (♮)': '',
    'Flat (♭)': 'es',
    'Double-sharp(x)': 'isis',
    'Double-flat(♭♭)': 'eses'
};

// Maps suffixes to VexFlow accidentals
const suffixToVex = {
    'is': '#',
    '': 'n',
    'es': 'b',
    'isis': '##',
    'eses': 'bb'
};

const noteToSemitones = {
    'c': 0, 'bis': 0,
    'cis': 1, 'des': 1,
    'd': 2,
    'dis': 3, 'ees': 3,
    'e': 4, 'fes': 4,
    'f': 5, 'eis': 5,
    'fis': 6, 'ges': 6,
    'g': 7,
    'gis': 8, 'aes': 8,
    'a': 9,
    'ais': 10, 'bes': 10,
    'b': 11, 'ces': 11,
    'cisis': 2, 'deses': 0,
    'disis': 4, 'eeses': 2,
    'eisis': 6, 'feses': 3,
    'fisis': 7, 'geses': 5,
    'gisis': 9, 'aeses': 7,
    'aisis': 11, 'beses': 9,
    'bisis': 1, 'ceses': 11
};

// JUMP_CHART keys as "interval,semitones"
const jumpChart = {
    "2,1": "Diminished", "2,2": "Minor",
    "2,3": "Major", "2,4": "Augmented",
    
    "3,3": "Diminished", "3,4": "Minor",
    "3,5": "Major", "3,6": "Augmented",
    
    "4,5": "Diminished",
    "4,6": "Perfect", "4,7": "Augmented",
    
    "5,7": "Diminished",
    "5,8": "Perfect", "5,9": "Augmented",
    
    "6,8": "Diminished", "6,9": "Minor",
    "6,10": "Major", "6,11": "Augmented",
    
    "0,10": "Diminished", "0,11": "Minor",
    "0,12": "Major", "0,13": "Augmented",
    
    "1,2": "Diminished",
    "1,13": "Perfect", "1,14": "Augmented",
    "1,1": "Perfect", "1,12": "Augmented"
};

const octaveMap = {
    "c,": 2,
    "c": 3,
    "c'": 4,
    "c''": 5
};

const numPlacement = {
    '1': "Unison", '2': "Second",
    '3': "Third", '4': "Fourth",
    '5': "Fifth", '6': "Sixth",
    '7': "Seventh", '8': "Octave", '9': "Ninth",
    '10': "Tenth", '11': "Eleventh", '12': "Twelfth",
    '13': "Thirteenth", '14': "Fourteenth", '15': "Compound Octave",
    '16': "Sixteenth", '17': "Seventeenth", '18': "Eighteenth",
    '19': "Nineteenth", '20': "Twentieth", '21': "Twenty-first",
    '22': "2 Compound Octaves", '23': "Twenty-third", '24': "Twenty-fourth",
    '25': "Twenty-fifth", '26': "Twenty-sixth", '27': "Twenty-seventh",
    '28': "Twenty-eighth", '29': "3 Compound Octaves"
};

const userIntervals = ["--", "Unison", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Octave", "Ninth",
    "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Compound Octave",
    "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth", "Twenty-first",
    "2 Compound Octaves", "Twenty-third", "Twenty-fourth", "Twenty-fifth", "Twenty-sixth", "Twenty-seventh",
    "Twenty-eighth", "3 Compound Octaves"];

const userQualities = ["--", "Diminished", "Minor", "Perfect", "Major", "Augmented"];

const difficultySettings = {
    "Beginner": { clefs: ["treble", "bass"], sameClef: true, accs: ['Natural (♮)'], compound: false },
    "Intermediate": { clefs: ["treble", "bass"], sameClef: true, accs: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)'], compound: false },
    "Advanced": { clefs: ["treble", "bass"], sameClef: false, accs: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)'], compound: true },
    "C clef Fanfare": { clefs: ["tenor", "alto"], sameClef: true, accs: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)'], compound: false },
    "Accidental Fanfare": { clefs: ["treble", "bass"], sameClef: true, accs: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)', 'Double-sharp(x)', 'Double-flat(♭♭)'], compound: true },
    "Expert": { clefs: ["treble", "alto", "tenor", "bass"], sameClef: false, accs: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)', 'Double-sharp(x)', 'Double-flat(♭♭)'], compound: true }
};

function calculateInterval(octave1Str, octave2Str, pos1, pos2) {
    const o1 = octaveMap[octave1Str];
    const o2 = octaveMap[octave2Str];
    
    if (o1 === o2) {
        if (pos1 > pos2) return pos1 - pos2 + 1;
        else if (pos1 < pos2) return pos2 - pos1 + 1;
        else return 1;
    } else if (o1 > o2) {
        if (pos1 !== pos2) return (pos1 - pos2) + ((o1 - o2) * 8);
        else return (o1 - o2) * 8;
    } else { // o1 < o2
        if (pos1 !== pos2) return pos2 - pos1 + ((o2 - o1) * 8) - 1;
        else return (o2 - o1) * 8;
    }
}

function calculateSemitone(note1, note2, letterIdx1, letterIdx2, octave1Str, octave2Str) {
    const s1 = noteToSemitones[note1];
    const s2 = noteToSemitones[note2];
    const o1 = octaveMap[octave1Str];
    const o2 = octaveMap[octave2Str];
    
    if (letterIdx1 === letterIdx2) {
        if (o1 < o2) return Math.abs(s2 - s1 - 1);
        else if (o1 > o2) return Math.abs(s1 - s2 - 1);
        else if (o1 === o2 && s1 !== s2) return 14;
    }
    
    if (s2 > s1) return s2 - s1 + 1;
    else if (s2 < s1) return s2 + 13 - s1;
    
    return 1;
}

function clefRange(clef) {
    const ranges = {
        "treble": ["c'", "c''"],
        "alto": ["c", "c'"],
        "tenor": ["c", "c'"],
        "bass": ["c,", "c"]
    };
    const options = ranges[clef] || ["c'", "c''"];
    return options[Math.floor(Math.random() * options.length)];
}

function lilypondToVex(letter, suffix, octaveStr) {
    const acc = suffixToVex[suffix];
    const octave = octaveMap[octaveStr];
    // VexFlow format: key/octave (e.g., c/4, c#/4)
    // Note: VexFlow expects lowercase keys.
    return {
        key: `${letter}/${octave}`,
        accidental: acc === 'n' ? 'n' : acc // explicit natural
    };
}

function generateQuestion(options = {}) {
    // Merge options with defaults
    // options can specify 'difficulty' OR explicit 'clefs', 'accs', etc.
    let settings = {};
    if (options.difficulty && difficultySettings[options.difficulty]) {
        settings = { ...difficultySettings[options.difficulty] };
    } else {
        // Default to Beginner
        settings = { ...difficultySettings["Beginner"] };
    }
    
    // Overrides
    if (options.clefs) settings.clefs = options.clefs;
    if (options.accs) settings.accs = options.accs;
    if (options.sameClef !== undefined) settings.sameClef = options.sameClef;
    if (options.compound !== undefined) settings.compound = options.compound;

    return generateIntervalData(settings.clefs, settings.accs, settings.sameClef, settings.compound);
}

function generateIntervalData(selectedClefs, selectedAccidentals, sameClef, compoundOctave) {
    if (!selectedClefs || selectedClefs.length === 0) selectedClefs = ["treble"];
    if (!selectedAccidentals || selectedAccidentals.length === 0) selectedAccidentals = ["Natural (♮)"];

    let loops = 0;
    while (loops < 200) { // Increased loop limit for safety
        loops++;
        const clef1 = selectedClefs[Math.floor(Math.random() * selectedClefs.length)];
        const clef2 = sameClef ? clef1 : selectedClefs[Math.floor(Math.random() * selectedClefs.length)];
        
        const fixOctave1 = clefRange(clef1);
        const fixOctave2 = compoundOctave ? clefRange(clef2) : fixOctave1;
        
        const accName1 = selectedAccidentals[Math.floor(Math.random() * selectedAccidentals.length)];
        const accName2 = selectedAccidentals[Math.floor(Math.random() * selectedAccidentals.length)];
        
        const suffix1 = accidentalNameMap[accName1];
        const suffix2 = accidentalNameMap[accName2];
        
        const letter1 = noteLetters[Math.floor(Math.random() * noteLetters.length)];
        const letter2 = noteLetters[Math.floor(Math.random() * noteLetters.length)];
        
        const note1Lily = (letter1 + suffix1).toLowerCase();
        const note2Lily = (letter2 + suffix2).toLowerCase();
        
        // Skip identical notes (mostly)
        if (note1Lily === note2Lily && fixOctave1 === fixOctave2) {
             if (Math.random() * 4 >= 1) { // 75% chance to skip
                 continue;
             }
        }
        
        const pos1 = noteLetters.indexOf(letter1);
        const pos2 = noteLetters.indexOf(letter2);
        
        let intervalNum = calculateInterval(fixOctave1, fixOctave2, pos1, pos2);
        const semitoneCount = calculateSemitone(note1Lily, note2Lily, pos1, pos2, fixOctave1, fixOctave2);
        
        // Correction logic from Python
        if (intervalNum >= 24) intervalNum -= 2;
        else if (intervalNum > 15 && intervalNum <= 23) intervalNum -= 1;
        
        const key = `${intervalNum % 7},${semitoneCount}`;
        
        if (jumpChart[key]) {
            const quality = jumpChart[key];
            const numberName = numPlacement[intervalNum.toString()];
            // Python: ans = f"{e_ans} {no_ans}"
            const answer = `${quality} ${numberName}`;
            
            return {
                answer,
                quality,
                intervalName: numberName,
                clef1,
                clef2,
                fixOctave1,
                fixOctave2,
                note1: note1Lily,
                note2: note2Lily,
                vexNote1: lilypondToVex(letter1, suffix1, fixOctave1),
                vexNote2: lilypondToVex(letter2, suffix2, fixOctave2)
            };
        }
    }
    // Fallback if loop fails (shouldn't happen often)
    return null;
}

function generate(options = {}) {
    const questionData = generateQuestion(options);
    const quality = questionData.quality;
    const interval = questionData.intervalName;
    const correctAnswer = `${quality} ${interval}`;

    return {
        questionText: `What is the interval between the two notes? (${questionData.note1} to ${questionData.note2})`,
        answerFormat: { type: 'composite', separator: ' ', fields: ['quality', 'interval'] },
        choices: {
            qualities: userQualities.filter(q => q !== '--'),
            intervals: userIntervals.filter(i => i !== '--')
        },
        correctAnswer,
        displayData: {
            vexNotes: [questionData.vexNote1, questionData.vexNote2],
            clefs: [questionData.clef1, questionData.clef2]
        },
        rawData: questionData
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
    accidentalNameMap
};
