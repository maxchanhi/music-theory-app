const harmonic_ascending = {
    'a': ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    'e': ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    'b': ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    'd': ['d', 'e', 'f', 'g', 'a', 'bf', 'cs'],
    'g': ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    'fs': ['fs', 'gs', 'a', 'b', 'cs', 'd', 'e'],
    'cs': ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b'],
    'c': ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    'f': ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    'gs': ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    'ds': ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'], 
    'bf': ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    'ef': ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd']
};

const harmonic_descending = {};
for (const [key, scale] of Object.entries(harmonic_ascending)) {
    harmonic_descending[key] = [scale[0], ...scale.slice(1).reverse()];
}

const melodic_ascending = {};
for (const [key, scale] of Object.entries(harmonic_ascending)) {
    let sixth = scale[5];
    let seventh = scale[6];

    // Modify 6th note
    if (!sixth.endsWith('s') && !sixth.endsWith('f')) {
        sixth += 's';
    } else if (sixth.endsWith('f')) {
        sixth = sixth.slice(0, -1);
    }

    // Modify 7th note (same logic as 6th usually, but here it seems we just take the 7th from harmonic which is already raised?)
    // Wait, harmonic minor has raised 7th. Melodic ascending has raised 6th AND 7th.
    // In harmonic_ascending map above, the 7th IS already raised (e.g., 'gs' for 'a' minor).
    // So for melodic ascending, we just need to raise the 6th based on the harmonic scale?
    // Let's check Python code:
    // scale[5][0] + 's' if scale[5][-1] != 's' and scale[5][-1] != 'f' else 
    // scale[5][0] if scale[5][-1] == 'f' else scale[5]
    // And it keeps scale[6] (7th) as is.
    // Yes, because harmonic already has raised 7th.
    
    melodic_ascending[key] = scale.slice(0, 5).concat([sixth, seventh]);
}

const melodic_descending = {};
for (const [key, scale] of Object.entries(melodic_ascending)) {
    // Melodic descending is natural minor (flattened 6th and 7th relative to major, or just natural minor)
    // Python code: scale[:5] + ... wait.
    // Python code for melodic_descending:
    // key: [scale[0]] + scale[:0:-1] for key, scale in melodic_ascending.items()
    // WAIT. The Python code says `melodic_descending` is just the reverse of `melodic_ascending`.
    // THAT IS INCORRECT MUSIC THEORY. Melodic minor descends as Natural Minor.
    // BUT I must follow the Python code's logic to replicate the app's behavior, unless I want to fix the bug.
    // User asked to "translate", so I should probably replicate logic but maybe add a comment.
    // Let's look closer at `minor_scale.py`:
    // melodic_descending = { key: [scale[0]] + scale[:0:-1] for key, scale in melodic_ascending.items() }
    // This effectively reverses the melodic ascending scale.
    // So if A Melodic Asc is A B C D E F# G#, Descending would be A G# F# E D C B A.
    // This is "Jazz Melodic Minor". Classical Melodic Minor descends as Natural Minor.
    // Given the app seems simple, I'll stick to the Python implementation for now to ensure parity.
    melodic_descending[key] = [scale[0], ...scale.slice(1).reverse()];
}

const starting_pitch_easy = ['a', 'e', 'b', 'd', 'g'];
const starting_pitch_intermediate = ['fs', 'cs', 'c', 'f'];
const starting_pitch_hard = ['gs', 'ds', 'bf', 'ef'];

const minor_types = [
    "harmonic ascending", "harmonic descending",
    "melodic ascending", "melodic descending"
];

const key_list = ['c', 'g', 'd', 'a', 'e', 'b', 'fs', 'gf', 'cs', 'df', 'gs', 'af', 'ef', 'ds', 'bf', 'f'];

function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function addOctaveIndicators(tonic) {
    const minorType = getRandomElement(minor_types);
    let minorScale;

    if (minorType === "harmonic ascending") minorScale = [...harmonic_ascending[tonic]];
    else if (minorType === "harmonic descending") minorScale = [...harmonic_descending[tonic]];
    else if (minorType === "melodic ascending") minorScale = [...melodic_ascending[tonic]];
    else if (minorType === "melodic descending") minorScale = [...melodic_descending[tonic]];

    const ascending = minorType.includes("ascending");
    const descending = minorType.includes("descending");

    // Find index of 'c' to handle octave breaks
    const cIndex = minorScale.findIndex(note => note.startsWith('c'));

    if (ascending) {
        if (cIndex >= 2) {
            for (let i = cIndex; i < minorScale.length; i++) {
                minorScale[i] += "'";
            }
        } else if (cIndex === 1) {
            minorScale[0] += ',';
        }

        let lastNote = minorScale[0];
        // In Python: if ',' in last_note: append(last_note.replace(',', '')) else: append(last_note + "'")
        // This adds the octave note at the end
        if (lastNote.includes(',')) {
            minorScale.push(lastNote.replace(',', ''));
        } else {
            minorScale.push(lastNote + "'");
        }
    }

    if (descending) {
        if (cIndex >= 2) {
            for (let i = cIndex + 1; i < minorScale.length; i++) {
                minorScale[i] += ",";
            }
        } else {
            for (let i = 0; i <= cIndex; i++) {
                minorScale[i] += "'";
            }
        }
        
        let firstNote = minorScale[0];
        // This adds the octave note at the end (which is the bottom tonic for descending)
        if (firstNote.includes("'")) {
            minorScale.push(firstNote.replace("'", ""));
        } else {
            minorScale.push(firstNote + ",");
        }
    }

    return { minorType, minorScale };
}

function pickClefRange() {
    const clefs = ['treble', 'alto', 'tenor', 'bass'];
    const clef = getRandomElement(clefs);
    let fixedPitch;

    if (clef === 'treble') fixedPitch = "c''";
    else if (clef === 'alto') fixedPitch = "c'";
    else if (clef === 'tenor') fixedPitch = "c";
    else fixedPitch = "c,";

    return { clef, fixedPitch };
}

function optionGeneration(startingPitch, ansDir, optionList) {
    let userOptions = [`${startingPitch} ${ansDir.split(' ')[0]} minor`];
    
    // Safety check to prevent infinite loop if optionList is too small
    let maxAttempts = 100;
    
    while (userOptions.length < 4 && maxAttempts > 0) {
        maxAttempts--;
        const newOption = getRandomElement(optionList);
        const newDir = getRandomElement(minor_types);
        const minorType = newDir.split(' ')[0]; // e.g. "harmonic" from "harmonic ascending"
        
        if (optionList.length > 8) {
            const idx1 = key_list.indexOf(startingPitch);
            const idx2 = key_list.indexOf(newOption);
            if (idx1 !== -1 && idx2 !== -1) {
                const distance = Math.abs(idx1 - idx2);
                if (distance <= 1 || distance >= key_list.length - 1) {
                    continue;
                }
            }
        }
        
        const option = `${newOption} ${minorType} minor`;
        if (!userOptions.includes(option)) {
            userOptions.push(option);
        }
    }
    
    // Shuffle options
    for (let i = userOptions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [userOptions[i], userOptions[j]] = [userOptions[j], userOptions[i]];
    }
    
    return userOptions;
}

function displayNote(note) {
    if (!note) return "";
    if (note.length === 2) {
        if (note[1] === 'f') return note[0].toUpperCase() + "-flat";
        if (note[1] === 's') return note[0].toUpperCase() + "-sharp";
    }
    return note.toUpperCase();
}

function generateQuestionData(level = "easy") {
    let optionList;
    if (level === "easy") optionList = starting_pitch_easy;
    else if (level === "intermediate") optionList = [...starting_pitch_intermediate, ...starting_pitch_easy];
    else optionList = [...starting_pitch_hard, ...starting_pitch_intermediate];

    const startingPitch = getRandomElement(optionList);
    const { clef, fixedPitch } = pickClefRange();
    const { minorType, minorScale } = addOctaveIndicators(startingPitch);
    
    const userOptions = optionGeneration(startingPitch, minorType, optionList);

    return {
        clef,
        startingPitch,
        minorType,
        minorScale,
        fixedPitch,
        userOptions
    };
}

module.exports = {
    generateQuestionData,
    displayNote
};
