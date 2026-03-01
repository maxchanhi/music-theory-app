// Helper to get random item from array
const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

// Helper to get n random items from array
const getRandomElements = (arr, n) => {
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
};

// Helper to shuffle array
const shuffleArray = (arr) => {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
};

const CLEFS = ['treble', 'bass', 'alto', 'tenor'];
const NOTES = ['c', 'd', 'e', 'f', 'g', 'a', 'b'];

const generateQuestion = () => {
    // 1. Pick 3 distinct clefs
    // Logic from python: picked_clefs = random.choice([clefs[1:], clefs[:3]])
    // clefs[1:] is ['alto','tenor','treble'] (no bass)
    // clefs[:3] is ['bass','alto','tenor'] (has bass)
    // Actually the python code says:
    // clefs=['bass','alto','tenor','treble']
    // if "bass" in picked_clefs: use C3/C4. Else use C4/C5.
    
    // We'll just pick any 3 distinct clefs for better variety, or stick to python logic?
    // Let's stick closer to python logic to ensure readability on staves.
    // If we mix Treble (high) and Bass (low) with C5, Bass will be crazy high ledger lines.
    
    // Python Logic:
    // Option 1: ['alto', 'tenor', 'treble'] -> Ref C4, C5
    // Option 2: ['bass', 'alto', 'tenor'] -> Ref C3, C4
    
    const clefSets = [
        ['alto', 'tenor', 'treble'],
        ['bass', 'alto', 'tenor']
    ];
    
    let selectedClefs = getRandomElement(clefSets);
    shuffleArray(selectedClefs); // e.g. ['treble', 'alto', 'tenor']
    
    // Determine Octaves
    let octaves;
    if (selectedClefs.includes('bass')) {
        octaves = [3, 4]; // C3, C4
    } else {
        octaves = [4, 5]; // C4, C5
    }
    
    // 2. Select Target Octave and Distractor Octave
    // add_idx = random.randint(0, 1)
    // target = octaves[add_idx]
    // distractor = octaves[1 - add_idx]
    const targetIdx = Math.floor(Math.random() * 2);
    const targetOctave = octaves[targetIdx];
    const distractorOctave = octaves[1 - targetIdx];
    
    // 3. Generate Melody (sequence of notes)
    // melody = [] while len < 4 ...
    const melodyLength = 4;
    const melodyNotes = [];
    while (melodyNotes.length < melodyLength) {
        const n = getRandomElement(NOTES);
        // Python code ensures unique notes in melody? "if note not in melody"
        if (!melodyNotes.includes(n)) {
            melodyNotes.push(n);
        }
    }
    
    // 4. Construct Options
    // We need 3 options.
    // Option 0: Target Octave, Clef A (Same 1)
    // Option 1: Target Octave, Clef B (Same 2)
    // Option 2: Distractor Octave, Clef C (Diff)
    
    // We have 3 selected clefs. Let's assign them.
    // Python:
    // add_ref = [[picked_ref[add_idx], 'same_1'], [picked_ref[add_idx], 'same_2'], [picked_ref[1 - add_idx], 'diff']]
    // for idx, clef in enumerate(picked_clefs): add_ref[idx].append(clef)
    
    // So:
    // Item 0: Target Octave, selectedClefs[0], type='same'
    // Item 1: Target Octave, selectedClefs[1], type='same'
    // Item 2: Distractor Octave, selectedClefs[2], type='diff'
    
    const optionsRaw = [
        { octave: targetOctave, clef: selectedClefs[0], type: 'same', id: 'A' },
        { octave: targetOctave, clef: selectedClefs[1], type: 'same', id: 'B' },
        { octave: distractorOctave, clef: selectedClefs[2], type: 'diff', id: 'C' }
    ];
    
    // Shuffle options so "diff" isn't always last
    const options = shuffleArray(optionsRaw).map((opt, index) => {
        // Generate VexFlow keys for this option
        // Note: melodyNotes is ['c', 'd', ...]
        // VexFlow key: "c/4"
        const keys = melodyNotes.map(noteLetter => `${noteLetter}/${opt.octave}`);
        
        return {
            id: index, // 0, 1, 2 for frontend identification
            clef: opt.clef,
            keys: keys,
            type: opt.type,
            octave: opt.octave // useful for debugging
        };
    });
    
    return {
        options: options,
        melodyNotes: melodyNotes
    };
};

module.exports = {
    generateQuestion
};
