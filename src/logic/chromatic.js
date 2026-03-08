const alphabet = ["c", "d", "e", "f", "g", "a", "b"];
const black_white_key = {
    0: ['c'], 1: ['cs', 'df'], 2: ['d'], 3: ['ds', 'ef'],
    4: ['e'], 5: ['f', 'es'], 6: ['fs', 'gf'], 7: ['g'],
    8: ['gs', 'af'], 9: ['a'], 10: ['as', 'bf'], 11: ['b']
};

function generateChromaticScale(ascendingDir) {
    const startingPc = Math.floor(Math.random() * 12);
    const potentialStarts = black_white_key[startingPc];
    const startingPitch = potentialStarts[Math.floor(Math.random() * potentialStarts.length)];

    let scale = [startingPitch];
    let nextNum = startingPc;
    
    // Direction: 1 for ascending, -1 for descending
    const direction = ascendingDir ? 1 : -1;

    // We want 12 steps to reach the octave (13 notes total)
    // The loop runs until we have 12 unique pitches (the 13th is the octave of start)
    while (scale.length < 12) {
        // Move to next semitone
        nextNum = (nextNum + direction + 12) % 12;
        
        const potentialPitches = black_white_key[nextNum];
        // Pick random spelling
        const nextPitch = potentialPitches[Math.floor(Math.random() * potentialPitches.length)];
        
        if (scale.length >= 2) {
            // Python Logic: if next_pitch[0] == scale[-1][0] and next_pitch[0] == scale[-2][0]:
            // It means we have 3 notes with same letter (e.g. C, C#, C## - wait, C## isn't in our list, but C, Cs, Css? No.)
            // It means e.g. D, D#, Eb -> D, D, E. 
            // Actually, if we have D, D#, and we pick D## (not possible) or...
            // If we have C, C# and we pick C something? 
            // In our list, we have 'cs'/'df'.
            // If we have C, C# and next is D/Ebb? 
            // Wait, the logic is: prevent 3 consecutive notes starting with SAME char.
            // e.g. scale = [C, C#]. Next semitone is D (or C##/Ebb). 
            // If our list has D and Ebb? No, list has 'd'.
            // If list has 'cs' and 'df'.
            // If we are at C. Next is C# or Db.
            // If we pick C#, scale is [C, C#].
            // Next is D. List has 'd'.
            // If we picked Db. Scale is [C, Db]. Next is D.
            
            // The constraint is mostly for cases where we might pick a spelling that causes a run of 3.
            // e.g. E, E#, F -> E, E, F (ok).
            // e.g. F, Gb, G -> F, G, G (ok).
            // e.g. F, F#, Gb -> F, F, G (ok).
            // Wait, if we are at F, F#. Next is G (or F##).
            // If we pick F##, we have F, F, F. That's bad.
            
            if (nextPitch[0] === scale[scale.length - 1][0] && nextPitch[0] === scale[scale.length - 2][0]) {
                // Retry this step. 
                // Since nextNum was incremented at start of loop, we decrement it to "undo" the step
                // so next iteration increments it again and repicks.
                nextNum = (nextNum - direction + 12) % 12;
            } else {
                scale.push(nextPitch);
            }
        } else {
            scale.push(nextPitch);
        }
    }

    // Append Octave
    // Python: if "'" in scale[0] or "," not in scale[0]: append(scale[0]+"'")
    // This logic handles relative octave marking.
    // For VexFlow, we need to be careful.
    // If ascending, we end an octave higher.
    // If descending, we end an octave lower.
    
    const firstNote = scale[0];
    let lastNote = firstNote;
    
    if (ascendingDir) {
        // Add ' to indicate upper octave
        lastNote += "'"; 
    } else {
        // Add , to indicate lower octave
        lastNote += ",";
    }
    scale.push(lastNote);

    return scale;
}

function generateWrongOptions(originalScale, ascendingDir) {
    let wrongOptions = [];
    let usedIdx = new Set();
    while (wrongOptions.length < 3) { // 3 wrong + 1 correct = 4 total
        let idx = Math.floor(Math.random() * originalScale.length);
        if (usedIdx.has(idx)) continue;
        usedIdx.add(idx);

        let chromaticScale = [...originalScale];
        if (ascendingDir) {
            chromaticScale = wrongAscending(idx, chromaticScale);
        } else {
            chromaticScale = wrongDescending(idx, chromaticScale);
        }
        wrongOptions.push(chromaticScale);
    }
    return wrongOptions;
}

function wrongAscending(idx, chromaticScale) {
    let currentNote = chromaticScale[idx];
    let letter = currentNote[0];
    let letterIdx = alphabet.indexOf(letter);
    let wrongLetter = alphabet[(letterIdx + 1) % alphabet.length];
    let octave = currentNote.includes(",") ? "," : currentNote.includes("'") ? "'" : "";
    
    let addAcc = Math.random() > 0.5 ? "s" : "f";
    
    if (currentNote.length === 1 || (!currentNote.includes("s") && !currentNote.includes("f"))) {
        chromaticScale[idx] = letter + addAcc;
    } else if (idx % 2 === 0) {
        chromaticScale[idx] = letter;
    } else {
        chromaticScale[idx] = wrongLetter + "f";
        if (wrongLetter === "c") {
            chromaticScale[idx] += "'";
        }
    }
    
    if (octave && !chromaticScale[idx].includes(octave)) {
        chromaticScale[idx] += octave;
    }
    return chromaticScale;
}

function wrongDescending(idx, chromaticScale) {
    let currentNote = chromaticScale[idx];
    let letter = currentNote[0];
    let letterIdx = alphabet.indexOf(letter);
    let wrongLetter = alphabet[(letterIdx + 1) % alphabet.length];
    let octave = currentNote.includes(",") ? "," : currentNote.includes("'") ? "'" : "";
    
    let addAcc = Math.random() > 0.5 ? "s" : "f";
    
    if (currentNote.length === 1 || (!currentNote.includes("s") && !currentNote.includes("f"))) {
        chromaticScale[idx] = letter + addAcc;
    } else if (idx % 2 === 0) {
        chromaticScale[idx] = letter;
    } else {
        chromaticScale[idx] = wrongLetter + "f";
        if (wrongLetter === "c") {
            chromaticScale[idx] += ",";
        }
    }
    
    if (octave && !chromaticScale[idx].includes(octave)) {
        chromaticScale[idx] += octave;
    }
    return chromaticScale;
}

module.exports = {
    generateChromaticScale,
    generateWrongOptions
};
