const note_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];

const accidentalsMap = {
    'Flat (♭)': 'b',
    'Natural (♮)': 'n',
    'Sharp (♯)': '#',
    'Double-sharp (x)': '##',
    'Double-flat (𝄫)': 'bb'
};

const accidentalsList = Object.keys(accidentalsMap);

const levels = {
    "basic": {
        clefs: ["treble", "bass"],
        accidentals: ['Natural (♮)']
    },
    "intermediate": {
        clefs: ["treble", "bass"],
        accidentals: ['Flat (♭)', 'Natural (♮)', 'Sharp (♯)']
    },
    "advanced": {
        clefs: ["treble", "bass"],
        accidentals: accidentalsList
    },
    "c clefs": {
        clefs: ["alto", "tenor"],
        accidentals: ['Natural (♮)']
    },
    "all clefs": {
        clefs: ["treble", "alto", "tenor", "bass"],
        accidentals: accidentalsList
    }
};

// Data from element.py
// pitch_range: c' means "c" is C4. c means "c" is C3.
const clefsData = {
    "treble": {
        "instaff": ['d', 'e', 'f', 'g', 'a', 'b', "c'", "d'", "e'", "f'", "g'"],
        "leger_lines": ["g,", "a,", "b,", "c", "a'", "b'", "c''", "d''"], 
        "pitch_range": "c'"
    },
    "bass": {
        "instaff": ['f,', 'g,', 'a,', 'b,', "c", "d", "e", "f", "g", "a", "b"],
        "leger_lines": ["c,", "d,", "e,", "c'", "d'", "e'", "f'"], 
        "pitch_range": "c"
    },
    "tenor": {
        "instaff": ["c,", 'd,', 'e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f"],
        "leger_lines": ["g,,", "a,,", "b,,", "g", "a", "b", "c''"], 
        "pitch_range": "c'"
    },
    "alto": {
        "instaff": ['e,', 'f,', 'g,', 'a,', 'b,', "c", "d", "e", "f", "g", 'a'],
        "leger_lines": ["c,", 'd,', "b", "c'", "d'", "e'"], 
        "pitch_range": "c'"
    }
};

/**
 * Converts a LilyPond-style pitch string (relative to a fixed point) to VexFlow key.
 * @param {string} noteStr - e.g. "c", "c'", "c,"
 * @param {string} rangeBase - "c'" (C4) or "c" (C3)
 * @returns {string} - VexFlow key e.g. "c/4"
 */
function convertToVexFlow(noteStr, rangeBase) {
    let baseOctave = (rangeBase === "c'") ? 4 : 3;
    
    // Count apostrophes and commas
    const octUp = (noteStr.match(/'/g) || []).length;
    const octDown = (noteStr.match(/,/g) || []).length;
    
    let octave = baseOctave + octUp - octDown;
    let note = noteStr.replace(/['+,]/g, '').toLowerCase();
    
    return `${note}/${octave}`;
}

function generateQuestion(options) {
    // options: { difficulty: string, useLedger: boolean, selectedClefs: [], selectedAccidentals: [] }
    
    let poolClefs = options.selectedClefs;
    let poolAccidentals = options.selectedAccidentals;
    
    // Defaults if not provided
    if (!poolClefs || poolClefs.length === 0) poolClefs = ["treble"];
    if (!poolAccidentals || poolAccidentals.length === 0) poolAccidentals = ['Natural (♮)'];
    
    const chosenClef = poolClefs[Math.floor(Math.random() * poolClefs.length)];
    const clefInfo = clefsData[chosenClef];
    
    const chosenAccidentalLabel = poolAccidentals[Math.floor(Math.random() * poolAccidentals.length)];
    const vexAccidental = accidentalsMap[chosenAccidentalLabel];
    
    const noteList = options.useLedger ? clefInfo.leger_lines : clefInfo.instaff;
    // Fallback if ledger lines requested but empty (though data seems populated)
    const validNoteList = (noteList && noteList.length > 0) ? noteList : clefInfo.instaff;
    
    const chosenNoteRaw = validNoteList[Math.floor(Math.random() * validNoteList.length)];
    
    // Convert raw note to VexFlow key (without accidental yet)
    const vexKeyBase = convertToVexFlow(chosenNoteRaw, clefInfo.pitch_range);
    
    // Construct final VexFlow key with accidental
    // VexFlow key format: "c/4", "c#/4", "cb/4"
    // But we usually attach accidental separately or as part of key?
    // standard VexFlow keys are "c/4", "db/4".
    // Accidental is added via .addModifier.
    
    // We need to return the answer as "Note Letter + Accidental"
    // chosenNoteRaw e.g. "c'" -> Note is C.
    const noteLetter = chosenNoteRaw.replace(/['+,]/g, '').toUpperCase();
    
    return {
        clef: chosenClef,
        vexKey: vexKeyBase, // e.g. "c/4"
        accidental: vexAccidental, // e.g. "#", "n"
        answer: {
            note: noteLetter,
            accidental: chosenAccidentalLabel
        }
    };
}

module.exports = {
    levels,
    note_letters,
    accidentalsList,
    generateQuestion
};
