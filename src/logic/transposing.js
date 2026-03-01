// Music theory constants and helper functions for transposition

const MAJOR_KEYS = ['g major', 'd major', 'a major', 'ef major', 'bf major', 'ef major'];
const MINOR_KEYS = ['e minor', 'b minor', 'fs minor', 'c minor', 'g minor', 'd minor', 'fs minor'];
const TRANSPOSITIONS = ["up a major 2nd", "down a minor 3rd", "up a perfect 5th"];
const ALPHABET = ["c", "d", "e", "f", "g", "a", "b"];

// Mapping from scale name to notes
const KEY_SCALES = {
    "c major": ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    "a minor": ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    "g major": ['g', 'a', 'b', 'c', 'd', 'e', 'fs'],
    "e minor": ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    "d major": ['d', 'e', 'fs', 'g', 'a', 'b', 'cs'],
    "b minor": ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    "a major": ['a', 'b', 'cs', 'd', 'e', 'fs', 'gs'],
    "fs minor": ['fs', 'gs', 'a', 'b', 'cs', 'd', 'es'],
    "e major": ['e', 'fs', 'gs', 'a', 'b', 'cs', 'ds'],
    "cs minor": ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'bs'],
    "b major": ['b', 'cs', 'ds', 'e', 'fs', 'gs', 'as'],
    "gs minor": ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    "fs major": ['fs', 'gs', 'as', 'b', 'cs', 'ds', 'es'],
    "ds minor": ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'],
    "gf major": ['gf', 'af', 'bf', 'cf', 'df', 'ef', 'f'],
    "ef minor": ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd'],
    "df major": ['df', 'ef', 'f', 'gf', 'af', 'bf', 'c'],
    "bf minor": ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    "af major": ['af', 'bf', 'c', 'df', 'ef', 'f', 'g'],
    "f minor": ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    "ef major": ['ef', 'f', 'g', 'af', 'bf', 'c', 'd'],
    "c minor": ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    "bf major": ['bf', 'c', 'd', 'ef', 'f', 'g', 'a'],
    "g minor": ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    "f major": ['f', 'g', 'a', 'bf', 'c', 'd', 'e'],
    "d minor": ['d', 'e', 'f', 'g', 'a', 'bf', 'cs']
};

const SEMITONES = {
    0: ['c', 'bs'], 1: ['cs', 'df'],
    2: ['d', 'css'], 3: ['ds', 'ef'],
    4: ['e', 'ff'], 5: ['f', 'es'],
    6: ['fs', 'gf'], 7: ['g', 'fss'],
    8: ['gs', 'af'], 9: ['a'],
    10: ['as', 'bf'], 11: ['b', 'cf']
};

const NOTE_TO_SEMITONES_LILYPOND = {
    'c': 0, 'bs': 0,
    'cs': 1, 'df': 1,
    'd': 2, 'css': 2,
    'ds': 3, 'ef': 3,
    'e': 4, 'ff': 4,
    'f': 5, 'es': 5,
    'fs': 6, 'gf': 6,
    'g': 7, 'fss': 7,
    'gs': 8, 'af': 8,
    'a': 9,
    'as': 10, 'bf': 10,
    'b': 11, 'cf': 11
};

// VexFlow mapping for accidentals
// python uses: 'fs', 'bf', 's', 'f' etc.
// VexFlow uses: '#', 'b', 'n', '##', 'bb'
// We need to convert our internal notation to VexFlow
const convertToVexFlow = (note) => {
    // note is like "c", "fs", "bf", "c'", "c,"
    // Remove octave markers for parsing
    let base = note.replace(/['+,]/g, '');
    let octave = 4; // Default middle C area
    
    // Check for octave shifts in original notation
    // In Python code: ' indicates up octave, , indicates down octave
    // Assuming base octave 4
    if (note.includes("'")) octave += 1;
    if (note.includes(",")) octave -= 1;
    
    let letter = base[0];
    let accidental = base.slice(1); // 's', 'f', 'ss', 'ff' or empty
    
    let vfAccidental = '';
    if (accidental === 's') vfAccidental = '#';
    else if (accidental === 'f') vfAccidental = 'b';
    else if (accidental === 'ss') vfAccidental = '##';
    else if (accidental === 'ff') vfAccidental = 'bb';
    
    return {
        key: `${letter}/${octave}`,
        accidental: vfAccidental
    };
};

const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

// count_alphabat
const countAlphabet = (oriNote, transposeBy) => {
    // oriNote e.g. "bf", "c"
    const note = oriNote[0];
    let pos = ALPHABET.indexOf(note);
    let newPos;
    
    if (transposeBy === "up a major 2nd") {
        newPos = pos + 1;
    } else if (transposeBy === "down a minor 3rd") {
        newPos = pos - 2;
    } else if (transposeBy === "up a perfect 5th") {
        newPos = pos + 4;
    } else if (transposeBy === "down a perfect 5th") {
        newPos = pos - 4;
    }
    
    let tranIdx = ((newPos % ALPHABET.length) + ALPHABET.length) % ALPHABET.length;
    let octave = "";
    
    if (newPos >= ALPHABET.length) {
        octave = "'";
    } else if (newPos < 0) {
        octave = ",";
    }
    
    return { letter: ALPHABET[tranIdx], octave };
};

// count_piano
const countPiano = (originalNote, newLetter, octave, transposeBy) => {
    // Clean original note
    let cleanNote = originalNote.replace(/['+,]/g, '');
    let semitoneIdx = NOTE_TO_SEMITONES_LILYPOND[cleanNote.toLowerCase()];
    
    let tranIdx;
    if (transposeBy === "up a major 2nd") {
        tranIdx = (semitoneIdx + 2) % 12;
    } else if (transposeBy === "down a minor 3rd") {
        tranIdx = (semitoneIdx - 3 + 12) % 12; // Ensure positive
    } else if (transposeBy === "up a perfect 5th") {
        tranIdx = (semitoneIdx + 7) % 12;
    } else if (transposeBy === "down a perfect 5th") {
        tranIdx = (semitoneIdx - 7 + 12) % 12;
    }
    
    const enharmonics = SEMITONES[tranIdx];
    for (let note of enharmonics) {
        if (note[0] === newLetter.toLowerCase()) {
            return note + octave;
        }
    }
    return null; // Should not happen if logic is correct
};

// each_note_transposition
const eachNoteTransposition = (note, transposeBy) => {
    const { letter, octave } = countAlphabet(note, transposeBy);
    return countPiano(note, letter, octave, transposeBy);
};

// add_accidental
const addAccidental = (melody) => {
    const newMelody = [...melody];
    const picked = [];
    while (picked.length < 3 && picked.length < newMelody.length) {
        const idx = Math.floor(Math.random() * newMelody.length);
        if (!picked.includes(idx)) {
            if (newMelody[idx].includes('f') || newMelody[idx].includes('s')) {
                newMelody[idx] = newMelody[idx][0]; // Remove accidental
            } else {
                newMelody[idx] = newMelody[idx] + getRandomElement(['s', 'f']);
            }
            picked.push(idx);
        }
    }
    return newMelody;
};

// wrong_accdental
const wrongAccidental = (transposedMelody) => {
    const newMelody = [...transposedMelody];
    const idx = Math.floor(Math.random() * newMelody.length);
    const note = newMelody[idx];
    
    let octave = "";
    if (note.includes("'")) octave = "'";
    else if (note.includes(",")) octave = ",";
    
    // remove octave from note base
    let base = note.replace(/['+,]/g, '');
    
    if (!base.includes('s') && !base.includes('f')) {
        base = base[0] + getRandomElement(['s', 'f']);
    } else {
        base = base[0]; // remove accidental
    }
    
    newMelody[idx] = base + octave;
    return newMelody;
};

// wrong_letter
const wrongLetter = (transposedMelody) => {
    const newMelody = [...transposedMelody];
    const idx = Math.floor(Math.random() * newMelody.length);
    const note = newMelody[idx];
    
    let octave = "";
    if (note.includes("'")) octave = "'";
    else if (note.includes(",")) octave = ",";
    
    let base = note.replace(/['+,]/g, '');
    let accidental = base.slice(1);
    
    let alphaIdx = ALPHABET.indexOf(base[0]);
    alphaIdx += getRandomElement([-1, 1]);
    
    let newOctave = octave;
    if (alphaIdx >= ALPHABET.length) {
        alphaIdx = alphaIdx % ALPHABET.length;
        if (note.includes(",")) newOctave = "";
        else newOctave = "'";
    } else if (alphaIdx < 0) {
        alphaIdx = (alphaIdx + ALPHABET.length) % ALPHABET.length;
        if (note.includes("'")) newOctave = "";
        else newOctave = ",";
    }
    
    newMelody[idx] = ALPHABET[alphaIdx] + accidental + newOctave;
    return newMelody;
};

// wrong_key_sign
const wrongKeySign = (key) => {
    // key e.g. "bf minor"
    const parts = key.split(" ");
    const keyNote = parts[0];
    const keyType = parts[1];
    
    const wrongDir = getRandomElement(["up a perfect 5th", "down a perfect 5th"]);
    let wrongKey = eachNoteTransposition(keyNote, wrongDir);
    
    // Remove octaves for key signature
    wrongKey = wrongKey.replace(/['+,]/g, '');
    
    return wrongKey + " " + keyType;
};

// Main Generation Function
const generateQuestion = () => {
    const pickAKey = getRandomElement(MAJOR_KEYS);
    const scale = KEY_SCALES[pickAKey];
    
    let melody = [];
    // Generate melody of 6 notes
    while (true) {
        melody = [];
        for (let i = 0; i < 6; i++) {
            melody.push(getRandomElement(scale));
        }
        // Ensure some variety (more than 1 unique note)
        const uniqueNotes = new Set(melody);
        if (melody.length - uniqueNotes.size <= 1) {
            break;
        }
    }
    
    melody = addAccidental(melody);
    const transposingBy = getRandomElement(TRANSPOSITIONS);
    
    const transposedMelody = [];
    const noteSplit = pickAKey.split(" ");
    let transposedKeyNote = eachNoteTransposition(noteSplit[0], transposingBy);
    transposedKeyNote = transposedKeyNote.replace(/['+,]/g, '');
    const transposedKey = transposedKeyNote + " " + noteSplit[1];
    
    for (let note of melody) {
        transposedMelody.push(eachNoteTransposition(note, transposingBy));
    }
    
    if (transposedMelody.some(n => n === null)) {
        throw new Error("Transposition resulted in null note");
    }
    
    // Generate Options
    // Option 1: Correct Key, Wrong Accidental
    // Option 2: Correct Key, Wrong Letter
    // Option 3: Wrong Key, Correct Melody
    // Option 4: Wrong Key, Wrong Accidental
    // Option 5: Wrong Key, Wrong Letter
    
    // Note: Python options_main generates 5 distractor options
    // And adds the correct one separately in picture_generation logic
    
    // Let's create the correct option first
    const correctOption = {
        key: transposedKey,
        melody: transposedMelody,
        type: 'correct'
    };
    
    const options = [correctOption];
    
    // Distractors
    options.push({
        key: transposedKey,
        melody: wrongAccidental(transposedMelody),
        type: 'wrong_accidental'
    });
    
    options.push({
        key: transposedKey,
        melody: wrongLetter(transposedMelody),
        type: 'wrong_letter'
    });
    
    const wKey = wrongKeySign(transposedKey);
    options.push({
        key: wKey,
        melody: transposedMelody,
        type: 'wrong_key'
    });
    
    options.push({
        key: wKey,
        melody: wrongAccidental(transposedMelody),
        type: 'wrong_key_accidental'
    });
    
    // Shuffle options
    for (let i = options.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [options[i], options[j]] = [options[j], options[i]];
    }
    
    // Format for frontend
    return {
        originalKey: pickAKey,
        originalMelody: melody,
        transposingBy: transposingBy,
        options: options.map((opt, idx) => ({
            id: idx,
            key: opt.key,
            melody: opt.melody,
            type: opt.type,
            // Pre-calculate VexFlow data
            vexData: opt.melody.map(convertToVexFlow)
        })),
        originalVexData: melody.map(convertToVexFlow)
    };
};

module.exports = {
    generateQuestion
};
