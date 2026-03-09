

// Constants from notation.py
const easymode = ["C major","A minor" ,"D major","B minor", "F major","D minor", "G major","E minor",
                   "B-flat major","G minor"];
const intermediate = ["A major", "F-sharp minor",
                   "E major","C-sharp minor","B major","G-sharp minor",
                   "B-flat major","G minor", "E-flat major", "C minor",
                   "A-flat major","F minor", "D-flat major","B-flat minor"];
const hard = ['E major', 'C-sharp minor', 'B major', 'G-sharp minor', 'F-sharp major',
        'D-sharp minor', 'G-flat major', 'E-flat minor', 'D-flat major', 
        'B-flat minor', 'A-flat major', 'F minor'];

const funEmojiList = [
    "😂",  "🎉",   "🚀",  "🐱", 
    "🐶",  "🦄",  
    "🎶",  "😱","👼🏻","💃🏻","🐰","🐒","🐣","🦀","💥","✨","🥳",
    "🍦",  "🌟",  "👻",  
    "🎈",   "🎮",  "💩"
];

// Map duration strings to numeric values (relative to whole note = 1 or quarter = 1? 
// Python uses Fraction(1, 4) for "4" (quarter note). 
// So "1" is a whole note.
const durationsFraction = {
    "2": 0.5, // Half
    "4": 0.25, // Quarter
    "8": 0.125, // Eighth
    "16": 0.0625, // Sixteenth
    "4.": 0.375, // Dotted Quarter (0.25 * 1.5)
    "8.": 0.1875 // Dotted Eighth (0.125 * 1.5)
};

// Reverse mapping for VexFlow?
// VexFlow durations: "h", "q", "8", "16", "qd", "8d"
const durationToVexFlow = {
    "2": "h",
    "4": "q",
    "8": "8",
    "16": "16",
    "4.": "qd",
    "8.": "8d"
};

const keyscale = {
    "C major": ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    "A minor": ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    "G major": ['g', 'a', 'b', 'c', 'd', 'e', 'fs'],
    "E minor": ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    "D major": ['d', 'e', 'fs', 'g', 'a', 'b', 'cs'],
    "B minor": ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    "A major": ['a', 'b', 'cs', 'd', 'e', 'fs', 'gs'],
    "F-sharp minor": ['fs', 'gs', 'a', 'b', 'cs', 'd', 'es'],
    "E major": ['e', 'fs', 'gs', 'a', 'b', 'cs', 'ds'],
    "C-sharp minor": ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'bs'],
    "B major": ['b', 'cs', 'ds', 'e', 'fs', 'gs', 'as'],
    "G-sharp minor": ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    "F-sharp major": ['fs', 'gs', 'as', 'b', 'cs', 'ds', 'es'],
    "D-sharp minor": ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'],
    "G-flat major": ['gf', 'af', 'bf', 'cf', 'df', 'ef', 'f'],
    "E-flat minor": ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd'],
    "D-flat major": ['df', 'ef', 'f', 'gf', 'af', 'bf', 'c'],
    "B-flat minor": ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    "A-flat major": ['af', 'bf', 'c', 'df', 'ef', 'f', 'g'],
    "F minor": ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    "E-flat major": ['ef', 'f', 'g', 'af', 'bf', 'c', 'd'],
    "C minor": ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    "B-flat major": ['bf', 'c', 'd', 'ef', 'f', 'g', 'a'],
    "G minor": ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    "F major": ['f', 'g', 'a', 'bf', 'c', 'd', 'e'],
    "D minor": ['d', 'e', 'f', 'g', 'a', 'bf', 'cs']
};

// Helper to convert Python pitch syntax to VexFlow
// 'gs' -> 'g#'
// 'bf' -> 'bb'
// 'fss' -> 'f##'
function toVexFlowAccidental(note) {
    if (note.endsWith('ss')) return note.slice(0, -2) + '##';
    if (note.endsWith('s')) return note.slice(0, -1) + '#';
    if (note.length > 1 && note.endsWith('f')) return note.slice(0, -1) + 'b'; // Single flat
    return note;
}

// Logic functions from motif.py

function rhythmGeneration(allRhythmList, numberOfBeat, lowertime) {
    let availableList = [...allRhythmList];
    const beatAmount = 1 / lowertime; // Fraction(1, lowertime)
    let melody = [];
    let melodyDurationSum = 0;
    const targetDuration = numberOfBeat * beatAmount;

    // Safety counter to prevent infinite loop
    let safety = 0;
    while (melodyDurationSum < targetDuration - 0.0001 && safety < 1000) {
        safety++;
        // If no available rhythms fit the remaining time, reset list or break to avoid infinite loop
        if (availableList.length === 0) {

             break;
        }

        const rhythmChoice = availableList[Math.floor(Math.random() * availableList.length)];
        
        // Safety check if rhythmChoice is undefined (should not happen if availableList is checked)
        if (!rhythmChoice) break;
        
        melody.push(rhythmChoice);
        melodyDurationSum += durationsFraction[rhythmChoice];

        // Check if we completed a beat (using epsilon for float comparison)
        const remainder = melodyDurationSum % beatAmount;
        const isBeatComplete = remainder < 0.0001 || Math.abs(remainder - beatAmount) < 0.0001;

        if (isBeatComplete) {
            availableList = [...allRhythmList];
        } else {
            // Update available list based on remaining beat amount
            // remainingBeat = beatAmount - (melodyDurationSum % beatAmount)
            // Fix modulo for floats
            const currentMod = melodyDurationSum - Math.floor(melodyDurationSum / beatAmount) * beatAmount;
            const remainingBeat = beatAmount - currentMod;
            
            availableList = allRhythmList.filter(r => durationsFraction[r] <= remainingBeat + 0.0001);
        }
    }
    return melody;
}

function getMotif(melody, scale, lowertime) {
    // melody is list of [pitch, duration]
    const intervalList = [];
    for (let i = 0; i < melody.length - 1; i++) {
        const idx1 = scale.indexOf(melody[i][0]);
        const idx2 = scale.indexOf(melody[i+1][0]);
        intervalList.push(Math.abs(idx1 - idx2));
    }

    let value = 0;
    let k = 0;
    const rhythmList = [];
    const pList = [0];
    const beatAmount = 1 / lowertime;

    for (const note of melody) {
        value += durationsFraction[note[1]];
        // if value % beatAmount == 0
        const remainder = value % beatAmount;
        if (remainder < 0.0001 || Math.abs(remainder - beatAmount) < 0.0001) {
            pList.push(k + 1);
            value = 0;
        }
        k++;
    }

    for (let j = 0; j < pList.length - 1; j++) {
        const rhythm = [];
        const slice = melody.slice(pList[j], pList[j+1]);
        for (const el of slice) {
            rhythm.push(el[1]);
        }
        rhythmList.push(rhythm);
    }

    return { intervalList, rhythmList };
}

function melodyRhyGen(motif, uppertime = 4, lowertime = 4, bar = 2, rhythmList = []) {
    const beatSum = uppertime * (1 / lowertime) * bar;
    let motifSum = 0;
    let melody = [];

    for (const note of motif) {
        motifSum += durationsFraction[note[1]];
        melody.push([...note]); // Deep copy note [pitch, duration]
    }

    // If we have no rhythm list, we can't generate anything
    if (rhythmList.length === 0) return melody;

    let safety = 0;
    while (motifSum < beatSum - 0.0001 && safety < 1000) {
        safety++;
        const choice = rhythmList[Math.floor(Math.random() * rhythmList.length)];
        
        // Safety check
        if (!choice) break;

        for (const noteDur of choice) {
            motifSum += durationsFraction[noteDur];
            // Placeholder pitch, will be filled later
            melody.push(['c', noteDur]); 
        }
    }
    return melody;
}

function melodyRhyGenMixed(motif, uppertime = 4, lowertime = 4, bar = 2, rhythmList = []) {
    const beatSum = uppertime * (1 / lowertime) * bar;
    let motifSum = 0;
    let melody = [];

    for (const note of motif) {
        motifSum += durationsFraction[note[1]];
        melody.push([...note]); // [pitch, duration]
    }

    let safety = 0;
    while (motifSum < beatSum - 0.0001 && safety < 1000) {
        safety++;
        const choice = rhythmList[Math.floor(Math.random() * rhythmList.length)];
        for (const noteDur of choice) {
            motifSum += durationsFraction[noteDur];
            melody.push(noteDur); // Push string duration only
        }
    }
    return melody;
}

function insertNoteMixed(melody, intervalList, scale) {
    for (let i = 0; i < melody.length; i++) {
        let pitch;
        if (Array.isArray(melody[i])) {
            pitch = melody[i][0];
        } else {
            // It's a string duration. Find previous pitch.
            let j = i - 1;
            while (j >= 0) {
                if (Array.isArray(melody[j])) {
                    pitch = melody[j][0];
                    break;
                }
                j--;
            }
            if (j < 0) throw new Error("No previous pitch found.");
            
            const pitchPos = scale.indexOf(pitch);
            const interval = intervalList[Math.floor(Math.random() * intervalList.length)];
            // Randomly add or subtract interval? Python code:
            // n_pitch = (pitch_pos + random.choice(interval_list)) % len(scale)
            // Wait, Python's interval_list comes from abs(index1 - index2). It's always positive.
            // So it always goes UP or wraps around?
            // Python: `n_pitch = (pitch_pos + random.choice(interval_list)) % len(scale)`
            // Yes, it strictly adds. This implies the melody tends to ascend or wrap around.
            
            const nPitchIndex = (pitchPos + interval) % scale.length;
            const newPitch = scale[nPitchIndex];
            
            melody[i] = [newPitch, melody[i]]; // Convert string to [pitch, duration]
        }
    }
    return melody;
}

function checkContour(melody, scale) {
    let tonic = false, dominant = false, mediant = false, leading = false;
    // Scale indices: 0 (tonic), 2 (mediant), 4 (dominant), 6 (leading)
    const tonicPitch = scale[0];
    const mediantPitch = scale[2];
    const dominantPitch = scale[4];
    const leadingPitch = scale[6];

    for (const note of melody) {
        const p = note[0];
        if (p === tonicPitch) tonic = true;
        else if (p === mediantPitch) mediant = true;
        else if (p === dominantPitch) dominant = true;
        else if (p === leadingPitch) leading = true;
    }
    return tonic && mediant && dominant && leading;
}

function generateSingleMelody(key) {
    try {
        const rhythmList = ["4", "8", "8.", "16"];
        const scale = keyscale[key];
        
        const rhyMotif = rhythmGeneration(rhythmList, 2, 4);
        // Safety check if rhythm generation failed
        if (!rhyMotif || rhyMotif.length === 0) {
            console.error("rhythmGeneration failed to produce rhythm");
            return null;
        }

        let melody = [];
        for (const dur of rhyMotif) {
            melody.push([scale[Math.floor(Math.random() * scale.length)], dur]);
        }
        
        const { intervalList, rhythmList: motifRhythmList } = getMotif(melody, scale, 4);
        
        // Generate full melody (mixed format)
        let fullMelody = melodyRhyGenMixed(melody, 4, 4, 2, motifRhythmList);
        
        // Safety check if fullMelody generation failed
        if (!fullMelody || fullMelody.length === 0) {
            console.error("melodyRhyGenMixed failed to produce full melody");
            return null;
        }

        // Insert notes
        fullMelody = insertNoteMixed(fullMelody, intervalList, scale);
        
        return fullMelody;
    } catch (err) {
        console.error("Error in generateSingleMelody:", err);
        return null;
    }
}

function mainGeneration(key) {
    const scale = keyscale[key];
    let bestMelody = null;
    
    // Try to generate a melody that satisfies contour check
    // Retry loop for contour check
    let safety = 0;
    while (safety < 100) {
        safety++;
        const melody = generateSingleMelody(key);
        if (melody) {
            bestMelody = melody;
            if (checkContour(melody, scale)) {
                return melody;
            }
        }
    }
    
    console.warn(`Could not satisfy contour check for key ${key} after 100 attempts. Returning best effort.`);
    
    if (bestMelody) {
        return bestMelody;
    }
    
    // Extreme fallback if everything failed
    console.error(`Failed to generate any melody for key ${key}. returning simple scale.`);
    return scale.slice(0, 4).map(p => [p, "4"]);
}

function generateOptions(ansKey, filteredKeyscaleKeys) {
    const options = [];
    const allKeys = Object.keys(keyscale);
    const ansKeyIndex = allKeys.indexOf(ansKey);
    
    // Shuffle filtered keys to get random candidates
    const candidates = [...filteredKeyscaleKeys].sort(() => 0.5 - Math.random());
    
    for (const key of candidates) {
        if (key !== ansKey) {
            const keyIndex = allKeys.indexOf(key);
            if (Math.abs(keyIndex - ansKeyIndex) > 1) {
                options.push(key);
            }
        }
        if (options.length === 3) break; // We need 3 distractors + 1 correct = 4 total
    }
    
    // If we don't have enough options (e.g. small difficulty set), just fill with whatever
    while (options.length < 3) {
        const randomKey = candidates[Math.floor(Math.random() * candidates.length)];
        if (randomKey !== ansKey && !options.includes(randomKey)) {
            options.push(randomKey);
        }
        if (options.length === candidates.length - 1) break; // Max possible
    }

    options.push(ansKey);
    return options.sort(() => 0.5 - Math.random());
}

// Convert melody to VexFlow format
function mapToVexFlow(melody) {
    // melody is list of [pitch, duration]
    // pitch is e.g. 'c', 'fs', 'bb'
    // duration is e.g. '4', '8.'
    
    return melody.map(note => {
        const pyPitch = note[0];
        const pyDur = note[1];
        
        // Convert pitch
        let vfPitch = toVexFlowAccidental(pyPitch);
        
        // Add octave (default 4)
        // Note: pyPitch is just class.
        // We should try to keep it in a reasonable range? 
        // For now, hardcode octave 4.
        const keys = [`${vfPitch}/4`];
        
        // Accidental?
        // VexFlow requires explicit accidental if not in key signature?
        // Or if we use `addModifier`.
        // The pitch string like `c#/4` is used for creation.
        // We need to extract the accidental for `addModifier`.
        
        let accidental = null;
        if (vfPitch.includes('##')) accidental = '##';
        else if (vfPitch.includes('#')) accidental = '#';
        else if (vfPitch === 'bb') accidental = 'b'; // Special case: 'bb' is B-flat
        else if (vfPitch.includes('bb')) accidental = 'bb';
        else if (vfPitch.length > 1 && vfPitch.endsWith('b')) accidental = 'b';
        else if (vfPitch.includes('n')) accidental = 'n';
        
        
        // Also map duration
        const duration = durationToVexFlow[pyDur];
        const isDotted = duration.includes('d');
        
        return {
            keys: keys,
            duration: duration,
            accidental: accidental,
            isDotted: isDotted
        };
    });
}

module.exports = {
    mainGeneration,
    generateOptions,
    mapToVexFlow,
    keyscale,
    easymode,
    intermediate,
    hard,
    funEmojiList
};
