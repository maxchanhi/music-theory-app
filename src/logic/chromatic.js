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
    let currentOctaveMod = "";
    
    // Direction: 1 for ascending, -1 for descending
    const direction = ascendingDir ? 1 : -1;

    // We want 12 steps to reach the octave (13 notes total)
    // The loop runs until we have 12 unique pitches (the 13th is the octave of start)
    while (scale.length < 12) {
        let prevNum = nextNum;
        // Move to next semitone
        nextNum = (nextNum + direction + 12) % 12;
        
        // Check for octave crossing
        if (ascendingDir) {
            // Crossed from B (11) to C (0) or similar wrap
            if (nextNum < prevNum) {
                currentOctaveMod += "'";
            }
        } else {
            // Crossed from C (0) to B (11) or similar wrap
            if (nextNum > prevNum) {
                currentOctaveMod += ",";
            }
        }
        
        const potentialPitches = black_white_key[nextNum];
        // Pick random spelling
        let nextPitch = potentialPitches[Math.floor(Math.random() * potentialPitches.length)];
        
        if (scale.length >= 2) {
            // Check for 3 consecutive same letters
            if (nextPitch[0] === scale[scale.length - 1][0] && nextPitch[0] === scale[scale.length - 2][0]) {
                // Retry this step. 
                nextNum = prevNum; // Reset index
                // Reset octave mod if we crossed boundary in this failed step?
                // Yes, if we crossed, we updated currentOctaveMod. We must revert it.
                // Actually, currentOctaveMod is cumulative string. 
                // Ascending: remove last '
                // Descending: remove last ,
                if (ascendingDir && ((nextNum + 1) % 12) < nextNum) { // Re-check condition? No, simplify.
                     // Easier to just not update currentOctaveMod until we confirm the note?
                     // Or revert:
                     if (ascendingDir && ((prevNum + 1)%12) < prevNum) currentOctaveMod = currentOctaveMod.slice(0, -1); 
                     // Wait, prevNum is the VALID note's index.
                     // If we fail, nextNum goes back to prevNum.
                     // We should recalculate crossover in next iteration.
                     // But we already modified `currentOctaveMod` outside.
                     // Let's refactor to calculate crossover locally first.
                }
                // Actually, easier refactor: Move crossover logic AFTER picking valid note?
                // No, the pitch depends on index which depends on crossover.
                
                // Let's revert the state if we retry
                 if (ascendingDir) {
                    if (((prevNum + 1) % 12) < prevNum) { // This was the condition that triggered
                        currentOctaveMod = currentOctaveMod.slice(0, -1);
                    }
                } else {
                    if (((prevNum - 1 + 12) % 12) > prevNum) {
                        currentOctaveMod = currentOctaveMod.slice(0, -1);
                    }
                }
                
                continue;
            }
        }

        // Check if we need to add a courtesy natural
        // If previous note has same letter and an accidental, and this one is natural
        const prevNote = scale[scale.length - 1];
        // prevNote might have octave chars now! Strip them for analysis
        const prevBase = prevNote.replace(/['+,]/g, '');
        
        const prevHasAcc = prevBase.length > 1 && (prevBase.includes('s') || prevBase.includes('f'));
        const nextIsNatural = nextPitch.length === 1;
        
        if (prevBase[0] === nextPitch[0] && prevHasAcc && nextIsNatural) {
            nextPitch += "n";
        }
        
        scale.push(nextPitch + currentOctaveMod);
    }

    // Append Octave
    const firstNote = scale[0];
    let lastNote = firstNote;
    
    if (ascendingDir) {
        // Add ' to indicate upper octave
        lastNote += "'"; 
        if (currentOctaveMod) lastNote += currentOctaveMod; // Add accumulated octaves? No, last note is relative to start.
        // Wait, if we accumulated octaves in the loop, the last note generated in loop already has them.
        // The 13th note (octave of start) should just be start + 1 octave relative to start.
        // But if start was C, and we went up to B (which got '), then next C needs ''.
        // Actually, my currentOctaveMod logic adds ' when crossing B->C.
        // So if we start at C, we cross B->C at the very end (for the 13th note).
        // The loop runs 12 times (generating 12 intervals, so 13 notes?). No, `scale` starts with 1 note.
        // Loop runs while len < 12. So it adds 11 notes. Total 12 notes (e.g. C ... B).
        // The 13th note is added here.
        
        // We need to calculate if 13th note crosses boundary too.
        let prevNum = nextNum;
        nextNum = (nextNum + direction + 12) % 12;
        if (nextNum < prevNum) currentOctaveMod += "'";
        
        // Reconstruct last note based on start pitch + current mod
        // But wait, start pitch string doesn't have accidental if it was natural.
        // If start was "cs", end is "cs" + mod.
        
        // Actually simpler: The 13th note is just the starting pitch but in the new octave context.
        // We just need to append currentOctaveMod.
        
        // BUT: `lastNote` variable here is `scale[0]`. `scale[0]` has no mod.
        // We should just use `scale[0] + currentOctaveMod`.
        // AND if we just crossed boundary for this last note, we need to add another ' ?
        // If start=C. Loop ends at B. `currentOctaveMod` is "".
        // 13th note is C. We cross B->C. `currentOctaveMod` becomes "'".
        // So we append "c" + "'". Correct.
        
        // If start=G. Loop ends at F#. `currentOctaveMod` is "'" (crossed at C).
        // 13th note is G. No cross F#->G. `currentOctaveMod` is "'".
        // We append "g" + "'". Correct.
        
        lastNote = scale[0] + currentOctaveMod;
    } else {
        // Descending
        let prevNum = nextNum;
        nextNum = (nextNum + direction + 12) % 12;
        if (nextNum > prevNum) currentOctaveMod += ",";
        
        lastNote = scale[0] + currentOctaveMod;
    }
    scale.push(lastNote);

    console.log(`[DEBUG] generateChromaticScale (${ascendingDir ? 'asc' : 'desc'}):`, JSON.stringify(scale));
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
