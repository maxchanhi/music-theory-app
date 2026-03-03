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
    
    melodic_ascending[key] = scale.slice(0, 5).concat([sixth, seventh]);
}

const melodic_descending = {};
for (const [key, scale] of Object.entries(melodic_ascending)) {
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

function addOctaveIndicators(tonic, clef) {
    const minorType = getRandomElement(minor_types);
    let minorScale;

    if (minorType === "harmonic ascending") minorScale = [...harmonic_ascending[tonic]];
    else if (minorType === "harmonic descending") minorScale = [...harmonic_descending[tonic]];
    else if (minorType === "melodic ascending") minorScale = [...melodic_ascending[tonic]];
    else if (minorType === "melodic descending") minorScale = [...melodic_descending[tonic]];

    const ascending = minorType.includes("ascending");
    const descending = minorType.includes("descending");

    // Base octave adjustment
    // Start by ensuring the relative octaves are correct (scale continuity)
    const cIndex = minorScale.findIndex(note => note.startsWith('c'));
    
    if (ascending) {
        // e.g. A B C ... -> a b c'
        if (cIndex >= 0) {
            for (let i = cIndex; i < minorScale.length; i++) {
                minorScale[i] += "'";
            }
        }
        
        // Add octave note at end
        let lastNote = minorScale[0];
        // If lastNote (tonic) has comma, remove it for the octave up. If it has ', add ''. 
        // But here we are working with base notes (no octave marks yet except what we just added).
        // Actually, we should strip existing octave markers to be safe before adding, 
        // but our arrays are clean.
        
        // Logic: if the first note didn't get a ' (because cIndex > 0), then the octave up gets a '.
        // If the first note got a ' (because it IS c), then octave up gets ''.
        
        // Let's simplify: construct the scale with proper relative octaves first.
    }
    
    // REWRITE: Construct absolute pitch chain first, then shift for clef.
    // 1. Clean scale (remove any stray marks if any)
    minorScale = minorScale.map(n => n.replace(/['+,]/g, ''));
    
    // 2. Build relative octave sequence (0 = base octave, 1 = next up)
    let octaveOffsets = [0];
    let currentOctave = 0;
    for (let i = 0; i < minorScale.length - 1; i++) {
        // If current note is B and next is C, octave increases
        const curr = minorScale[i][0]; // 'b'
        const next = minorScale[i+1][0]; // 'c'
        if (curr === 'b' && next === 'c') {
            currentOctave++;
        } else if (curr === 'c' && next === 'b') { // Descending break
            currentOctave--;
        }
        octaveOffsets.push(currentOctave);
    }
    
    // Add the final tonic octave (8th note)
    // For ascending, it should be +1 octave from start?
    // Wait, the arrays are 7 notes long. We need to add the 8th note.
    const root = minorScale[0];
    minorScale.push(root);
    
    // Calculate octave for 8th note
    const prev = minorScale[minorScale.length - 2][0];
    const last = minorScale[minorScale.length - 1][0];
    if (prev === 'b' && last === 'c') currentOctave++;
    else if (prev === 'c' && last === 'b') currentOctave--;
    octaveOffsets.push(currentOctave);

    // 3. Determine Base Octave for Clef
    // We want the scale to be centered in the staff.
    // Treble: C4-C5 (c' - c'')
    // Bass: C2-C3 (c, - c) or C3-C4
    // Alto: F3-F4 or C4-C5
    // Tenor: D3-D4 or A3-A4
    
    let baseOctaveShift = 0; 
    const pitchVal = "cdefgab".indexOf(tonic[0]);
    
    if (clef === 'treble') {
        // Range: C4 (c') to A5/B5
        // Start everything in 4th octave (c')
        baseOctaveShift = 1; 
    } else if (clef === 'bass') {
        // Range: E2 (e,) to C4 (c')
        // C, D, E -> Start at C3 (c) [0] or C2 (c,) [-1]?
        // C3 starts 2nd space. Goes to C4 (1 ledger line above). Good.
        // F, G, A, B -> Start at F2 (f,) [-1]. F2 is below staff. F3 is 4th line. Good.
        
        if (pitchVal <= 2) { // c, d, e
            baseOctaveShift = 0; // C3, D3, E3 start
        } else { // f, g, a, b
            baseOctaveShift = -1; // F2, G2, A2, B2 start
        }
    } else if (clef === 'alto') {
        // C4 is middle line.
        // F3 (f) to G4 (g').
        if (pitchVal <= 2) { // c, d, e
            baseOctaveShift = 1; // C4 start
        } else { // f, g, a, b
            baseOctaveShift = 0; // F3 start
        }
    } else if (clef === 'tenor') {
        // C4 is 4th line.
        // A2 (a,) to B3 (b).
        if (pitchVal <= 4) { // c, d, e, f, g
            baseOctaveShift = 0; // C3 start
        } else { // a, b
            baseOctaveShift = -1; // A2 start
        }
    }

    // 4. Apply octaves
    const finalScale = minorScale.map((n, i) => {
        let oct = octaveOffsets[i] + baseOctaveShift;
        let suffix = "";
        while (oct > 0) { suffix += "'"; oct--; }
        while (oct < 0) { suffix += ","; oct++; }
        return n + suffix;
    });

    return { minorType, minorScale: finalScale };
}

function pickClefRange() {
    const clefs = ['treble', 'alto', 'tenor', 'bass'];
    const clef = getRandomElement(clefs);
    let fixedPitch;

    // Fixed pitch for VexFlow stave connector if needed, or just visual reference
    if (clef === 'treble') fixedPitch = "c''";
    else if (clef === 'alto') fixedPitch = "c'";
    else if (clef === 'tenor') fixedPitch = "c";
    else fixedPitch = "c,";

    return { clef, fixedPitch };
}

function optionGeneration(startingPitch, ansDir, optionList) {
    let userOptions = [`${displayNote(startingPitch)} ${ansDir.split(' ')[0]} minor`];
    
    // Safety check to prevent infinite loop
    let maxAttempts = 100;
    
    while (userOptions.length < 4 && maxAttempts > 0) {
        maxAttempts--;
        const newOptionPitch = getRandomElement(optionList);
        const newDir = getRandomElement(minor_types);
        const minorType = newDir.split(' ')[0]; 
        
        const option = `${displayNote(newOptionPitch)} ${minorType} minor`;
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
    let cleanNote = note.replace(/['+,]/g, ''); // Remove octave markers
    if (cleanNote.length >= 2) {
        if (cleanNote.endsWith('f')) return cleanNote[0].toUpperCase() + "-flat";
        if (cleanNote.endsWith('s')) return cleanNote[0].toUpperCase() + "-sharp";
    }
    return cleanNote.toUpperCase();
}

function generateQuestionData(level = "easy") {
    let optionList;
    if (level === "easy") optionList = starting_pitch_easy;
    else if (level === "intermediate") optionList = [...starting_pitch_intermediate, ...starting_pitch_easy];
    else optionList = [...starting_pitch_hard, ...starting_pitch_intermediate];

    const startingPitch = getRandomElement(optionList);
    const { clef, fixedPitch } = pickClefRange();
    const { minorType, minorScale } = addOctaveIndicators(startingPitch, clef);
    
    const userOptions = optionGeneration(startingPitch, minorType, optionList);
    const answer = `${displayNote(startingPitch)} ${minorType.split(' ')[0]} minor`;

    return {
        clef,
        startingPitch,
        minorType,
        minorScale,
        fixedPitch,
        userOptions,
        answer
    };
}

module.exports = {
    generateQuestionData,
    displayNote
};
