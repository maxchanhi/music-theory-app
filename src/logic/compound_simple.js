const Fraction = require('fraction.js');

// Constants
const PITCH_LIST = ["e", "f", "g", "a", "b"];

const RHYTHM_SETTING = {
    "simple": ["4", "8 8", "\\tuplet 3/2 {8 8 8}", "\\tuplet 3/2 {4 8}", "\\tuplet 3/2 {8 4}", "8. 16"],
    "compound": ["4.", "\\tuplet 2/3 {8 8}", "8 8 8", "4 8", "8 4", "\\tuplet 2/3 {8. 16}"]
};

const TIME_SIGN_CAT = { 
    "simple duple": [["2/2",4], ["2/4",2]],
    "simple triple": [["3/2",6], ["3/4",3]],
    "simple quadruple": [["4/4",4], ["4/2",8]],
    "compound duple": [["6/4",6], ["6/8",3]],
    "compound triple": [ ["9/4",9], ["9/8",4.5]],
    "compound quadruple": [ ["12/8",6]]
};

function generateQuestionData() {
    // 1. Pick the time signature category
    const categories = Object.keys(TIME_SIGN_CAT);
    const timeSignCat = categories[Math.floor(Math.random() * categories.length)];
    const timeSignList = TIME_SIGN_CAT[timeSignCat];
    const timeSignData = timeSignList[Math.floor(Math.random() * timeSignList.length)];
    const timeSignature = timeSignData[0];
    const totalBeat = timeSignData[1];

    // 2. Pick the rhythm setting as the question
    let melodyRhythm = [];
    let beat = 0;
    let lastRhythm = null;

    while (beat < totalBeat) {
        if (timeSignCat.includes("simple")) {
            let availableRhythms = RHYTHM_SETTING["simple"].filter(r => r !== lastRhythm);
            if (availableRhythms.length === 0) availableRhythms = RHYTHM_SETTING["simple"];
            
            const rhythm = availableRhythms[Math.floor(Math.random() * availableRhythms.length)];
            melodyRhythm.push(rhythm);
            lastRhythm = rhythm;
            beat += 1;
        } else {
            let availableRhythms = RHYTHM_SETTING["compound"].filter(r => r !== lastRhythm);
            if (availableRhythms.length === 0) availableRhythms = RHYTHM_SETTING["compound"];
            
            const rhythm = availableRhythms[Math.floor(Math.random() * availableRhythms.length)];
            melodyRhythm.push(rhythm);
            lastRhythm = rhythm;
            beat += 1.5;
        }
    }

    // 3. Add random pitches to original melody
    const { pitchedMelody: finalQuestionMelody, pitches: questionPitches } = addPitches(melodyRhythm);

    // 4. Generate correct answer
    const isSimple = timeSignCat.includes("simple");
    const targetCatPrefix = isSimple ? "compound" : "simple";
    const catType = timeSignCat.split(' ')[1]; // duple, triple, quadruple
    const targetCat = `${targetCatPrefix} ${catType}`;
    
    const targetTimeSignList = TIME_SIGN_CAT[targetCat];
    const targetTimeSignData = targetTimeSignList[Math.floor(Math.random() * targetTimeSignList.length)];
    // Calculate correct target time signature based on simple <-> compound rule
    // Simple -> Compound: num * 3, den * 2
    // Compound -> Simple: num / 3, den / 2
    
    let correctTimeSig;
    const [qNum, qDen] = timeSignature.split('/').map(Number);
    
    if (isSimple) {
        correctTimeSig = `${qNum * 3}/${qDen * 2}`;
    } else {
        correctTimeSig = `${qNum / 3}/${qDen / 2}`;
    }

    const correctMelodyRhythm = tranSimpleCompound(melodyRhythm, timeSignCat, false);
    const finalCorrectMelody = applyPitchesToRhythm(correctMelodyRhythm, questionPitches);

    // 5. Generate wrong options
    const wrongOptionsData = generateWrongOptions(melodyRhythm, timeSignCat, correctMelodyRhythm, questionPitches, totalBeat);
    
    const options = [
        { timeSignature: correctTimeSig, notes: finalCorrectMelody, isCorrect: true, reason: "Correct translation" }
    ];

    for (const opt of wrongOptionsData) {
        if (options.length < 4) {
            const timeSig = opt.timeSignature || correctTimeSig;
            // Check uniqueness
            const exists = options.some(o => o.timeSignature === timeSig && JSON.stringify(o.notes) === JSON.stringify(opt.notes));
            if (!exists) {
                options.push({
                    timeSignature: timeSig,
                    notes: opt.notes,
                    isCorrect: false,
                    reason: "Incorrect modulation"
                });
            }
        }
    }

    // Ensure we have 4 options
    while (options.length < 4) {
        options.push({
            timeSignature: correctTimeSig,
            notes: applyPitchesToRhythm(melodyRhythm, questionPitches),
            isCorrect: false,
            reason: "Incorrect modulation"
        });
    }

    // Shuffle options
    const shuffledOptions = options.sort(() => Math.random() - 0.5);
    const correctIndex = shuffledOptions.findIndex(o => o.isCorrect);
    
    return {
        question: {
            timeSignature: timeSignature,
            notes: finalQuestionMelody
        },
        options: shuffledOptions,
        correctIndex
    };
}

function addPitches(rhythmList) {
    const pitchedMelody = [];
    const pitches = [];
    for (const segment of rhythmList) {
        if (segment.includes("tuplet")) {
            const startIdx = segment.indexOf("{") + 1;
            const endIdx = segment.indexOf("}");
            const prefix = segment.substring(0, startIdx);
            const content = segment.substring(startIdx, endIdx).trim();
            // Split by spaces, but preserve dotted notes if they are single tokens in the string
            // e.g. "8. 16" -> ["8.", "16"]
            // "8 8 8" -> ["8", "8", "8"]
            const notes = content.split(/\s+/);
            const pitchedNotes = notes.map(n => {
                const p = PITCH_LIST[Math.floor(Math.random() * PITCH_LIST.length)];
                pitches.push(p);
                return p + n;
            });
            pitchedMelody.push(`${prefix} ${pitchedNotes.join(' ')} }`);
        } else {
            const notes = segment.split(/\s+/);
            const pitchedNotes = notes.map(n => {
                const p = PITCH_LIST[Math.floor(Math.random() * PITCH_LIST.length)];
                pitches.push(p);
                return p + n;
            });
            pitchedMelody.push(pitchedNotes.join(' '));
        }
    }
    return { pitchedMelody, pitches };
}

function applyPitchesToRhythm(rhythmList, pitches) {
    const pitchedResult = [];
    let pitchIdx = 0;
    for (const segment of rhythmList) {
        if (segment.includes("tuplet")) {
            const startIdx = segment.indexOf("{") + 1;
            const endIdx = segment.indexOf("}");
            const prefix = segment.substring(0, startIdx);
            const content = segment.substring(startIdx, endIdx).trim();
            const notes = content.split(/\s+/);
            const pitchedNotes = notes.map(n => {
                const p = pitches[pitchIdx % pitches.length];
                pitchIdx++;
                return p + n;
            });
            pitchedResult.push(`${prefix} ${pitchedNotes.join(' ')} }`);
        } else {
            const notes = segment.split(/\s+/);
            const pitchedNotes = notes.map(n => {
                const p = pitches[pitchIdx % pitches.length];
                pitchIdx++;
                return p + n;
            });
            pitchedResult.push(pitchedNotes.join(' '));
        }
    }
    return pitchedResult;
}

function generateWrongOptions(originalRhythms, setting, correctRhythmList, pitches, totalBeat) {
    const wrongs = [];
    
    // New Strategy: If triple time, add an option in duple/quadruple with same total beats
    if (setting.includes("triple")) {
        const candidateSigns = [];
        for (const [cat, signs] of Object.entries(TIME_SIGN_CAT)) {
            if (cat.includes("duple") || cat.includes("quadruple")) {
                for (const [sign, beat] of signs) {
                    if (beat === totalBeat) {
                        candidateSigns.push(sign);
                    }
                }
            }
        }
        
        if (candidateSigns.length > 0) {
            const wrongTime = candidateSigns[Math.floor(Math.random() * candidateSigns.length)];
            wrongs.push({
                timeSignature: wrongTime,
                notes: applyPitchesToRhythm(originalRhythms, pitches),
                isCorrect: false
            });
        }
    }

    // Strategy 1: The original rhythm (no transformation)
    wrongs.push({
        timeSignature: null, // Will be set to targetTimeSign in caller
        notes: applyPitchesToRhythm(originalRhythms, pitches),
        isCorrect: false
    });
    
    // Strategy 2: Partially transformed
    if (originalRhythms.length > 1) {
        const partial = [...originalRhythms];
        partial[0] = correctRhythmList[0];
        wrongs.push({
            timeSignature: null,
            notes: applyPitchesToRhythm(partial, pitches),
            isCorrect: false
        });
    } else {
        const fallback = [...correctRhythmList];
        fallback[0] = fallback[0].replace("4.", "2").replace("4", "2");
        wrongs.push({
            timeSignature: null,
            notes: applyPitchesToRhythm(fallback, pitches),
            isCorrect: false
        });
    }

    // Strategy 3: Incorrect transformation
    const incorrect = originalRhythms.map(r => {
        if (!r.includes(' ') && !r.includes('.')) {
            return r.replace("4", "2");
        }
        return r;
    });
    wrongs.push({
        timeSignature: null,
        notes: applyPitchesToRhythm(incorrect, pitches),
        isCorrect: false
    });
    
    return wrongs;
}

function tranSimpleCompound(melody, setting, passStep = false, seed = 0) {
    const newMelody = [];
    let pass1 = false, pass2 = false, pass3 = false;
    if (passStep) {
        if (seed === 0) pass1 = true;
        else if (seed === 1) pass2 = true;
        else if (seed === 2) pass3 = true;
    }

    const isSimple = setting.includes("simple");
    if (isSimple) {
        for (const note of melody) {
            if (note.includes("tuplet")) {
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    const content = note.substring(startIdx, endIdx).trim();
                    newMelody.push(content);
                } else {
                    newMelody.push(note);
                }
            } else if (!note.includes(' ')) {
                if (!pass2) {
                    const match = note.match(/^([a-gA-G][s|f]?)(\d+)(\.*)$/);
                    if (match) {
                        newMelody.push(`${match[1]}${match[2]}.`);
                    } else {
                        newMelody.push(note + ".");
                    }
                } else {
                    newMelody.push(note);
                }
            } else {
                if (!pass3) {
                    newMelody.push(`\\tuplet 2/3 { ${note} }`);
                } else {
                    newMelody.push(note);
                }
            }
        }
    } else {
        for (const note of melody) {
            if (note.includes("tuplet")) {
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    const content = note.substring(startIdx, endIdx).trim();
                    newMelody.push(content);
                } else {
                    newMelody.push(note);
                }
            } else if (!note.includes(' ')) {
                if (!pass2) {
                    newMelody.push(note.replace('.', ''));
                } else {
                    newMelody.push(note);
                }
            } else {
                if (!pass3) {
                    newMelody.push(`\\tuplet 3/2 { ${note} }`);
                } else {
                    newMelody.push(note);
                }
            }
        }
    }
    return newMelody;
}

function getReason(seed) {
    if (seed === 0) return "Failed to remove tuplet/duplet notation";
    if (seed === 1) return "Failed to adjust note values (dots)";
    if (seed === 2) return "Failed to apply tuplet/duplet notation";
    return "Incorrect modulation";
}

module.exports = {
    generateQuestionData
};
