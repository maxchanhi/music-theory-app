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
        let prevNum = nextNum;
        nextNum = (nextNum + direction + 12) % 12;
        if (nextNum < prevNum) currentOctaveMod += "'";
    } else {
        let prevNum = nextNum;
        nextNum = (nextNum + direction + 12) % 12;
        if (nextNum > prevNum) currentOctaveMod += ",";
    }

    let lastNoteBase = scale[0];
    
    // Check if we need to add a courtesy natural for the final note
    const prevNote = scale[scale.length - 1];
    const prevBase = prevNote.replace(/['+,]/g, '');
    const prevHasAcc = prevBase.length > 1 && (prevBase.includes('s') || prevBase.includes('f'));
    const lastIsNatural = lastNoteBase.length === 1;
    
    if (prevBase[0] === lastNoteBase[0] && prevHasAcc && lastIsNatural) {
        lastNoteBase += "n";
    }
    
    lastNote = lastNoteBase + currentOctaveMod;
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

function generate(options = {}) {
    const ascending = options.ascending !== undefined ? options.ascending : Math.random() < 0.5;
    const clef = options.clef || 'treble';

    const chromaticScale = generateChromaticScale(ascending);
    const wrongOptions = generateWrongOptions(chromaticScale, ascending);

    const allOptions = [{ scale: chromaticScale, isCorrect: true }];
    wrongOptions.forEach((w, i) => {
        allOptions.push({ scale: w, isCorrect: false });
    });
    for (let i = allOptions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [allOptions[i], allOptions[j]] = [allOptions[j], allOptions[i]];
    }

    const correctIndex = allOptions.findIndex(o => o.isCorrect);

    return {
        questionText: `Which of these is the correct ${ascending ? 'ascending' : 'descending'} chromatic scale?`,
        answerFormat: { type: 'multiple-choice' },
        choices: allOptions.map(o => o.scale.join(' ')),
        correctAnswer: correctIndex,
        displayData: {
            clef,
            ascending,
            options: allOptions.map((o, i) => ({
                id: i,
                scale: o.scale,
                isCorrect: o.isCorrect
            }))
        },
        rawData: { options: allOptions, correctIndex, ascending, clef }
    };
}

function check(questionData, userAnswer) {
    const selectedIdx = typeof userAnswer === 'string' ? parseInt(userAnswer) : userAnswer;
    const correct = selectedIdx === questionData.correctIndex;

    return {
        correct,
        correctAnswer: questionData.correctIndex,
        explanation: correct
            ? 'Correct! That is the properly spelled chromatic scale.'
            : 'That is incorrect. The correct scale has the correct enharmonic spelling throughout.'
    };
}

const meta = {
    topic: 'chromatic',
    name: 'Chromatic Scales',
    description: 'Identify the correct chromatic scale notation',
    difficultyLevels: null,
    answerType: 'multiple-choice'
};

module.exports = {
    generateChromaticScale,
    generateWrongOptions,
    generate,
    check,
    meta
};
