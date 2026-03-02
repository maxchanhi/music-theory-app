const Fraction = require('fraction.js');

// Constants
const PITCH_LIST = ["e", "f", "g", "a", "b"];

const RHYTHM_SETTING = {
    "simple": ["4", "8 8", "\\tuplet 3/2 {8 8 8}", "\\tuplet 3/2 {4 8}", "\\tuplet 3/2 {8 4}", "8. 16"],
    "compound": ["4.", "\\tuplet 2/3 {8 8}", "8 8 8", "4 8", "8 4", "\\tuplet 2/3 {8. 16}"]
};

const TIME_SIGN_CAT = {
    "simple duple": ["2/2", "2/4", "2/8", "2/16"],
    "simple triple": ["3/2", "3/4", "3/8", "3/16"],
    "simple quadruple": ["4/2", "4/4", "4/8", "4/16"],
    "compound duple": ["6/2", "6/4", "6/8", "6/16"],
    "compound triple": ["9/2", "9/4", "9/8", "9/16"],
    "compound quadruple": ["12/2", "12/4", "12/8", "12/16"]
};

// Helper to adjust rhythms (e.g. double duration)
function adjustRhythms(rhythms, rate) {
    return rhythms.map(rhythm => {
        if (rhythm.includes("tuplet")) {
            const startIdx = rhythm.indexOf("{") + 1;
            const endIdx = rhythm.indexOf("}");
            const content = rhythm.substring(startIdx, endIdx).trim();
            const notes = content.split(/\s+/);
            
            const adjustedNotes = notes.map(note => {
                if (note.includes('.')) {
                    const base = parseInt(note.split('.')[0]);
                    return `${base * rate}.`;
                } else {
                    return `${parseInt(note) * rate}`;
                }
            });
            
            return `${rhythm.substring(0, startIdx)}${adjustedNotes.join(' ')}${rhythm.substring(endIdx)}`;
        } else {
            const parts = rhythm.split(/\s+/);
            const adjustedParts = parts.map(part => {
                if (part.includes('.')) {
                    const base = parseInt(part.split('.')[0]);
                    return `${base * rate}.`;
                } else {
                    return `${parseInt(part) * rate}`;
                }
            });
            return adjustedParts.join(' ');
        }
    });
}

function settingGeneration() {
    const categories = Object.keys(TIME_SIGN_CAT);
    const pickCat = categories[Math.floor(Math.random() * categories.length)];
    const timeSigns = TIME_SIGN_CAT[pickCat];
    
    // Skip first and last if possible to avoid extremes, matching Python
    let availableSigns = timeSigns;
    if (timeSigns.length > 2) {
        availableSigns = timeSigns.slice(1, -1);
    }
    
    const pickTimeSign = availableSigns[Math.floor(Math.random() * availableSigns.length)];
    const [numStr, denStr] = pickTimeSign.split('/');
    let numerator = parseInt(numStr);
    let denominator = parseInt(denStr);
    
    let pickRhySetting = [];
    
    // Logic matching Python's setting_generation
    
    if (pickCat.includes("compound")) {
        // Calculate number of beats
        numerator = numerator / 3;
    }
    
    // Determine rhythm list based on denominator
    if (denominator === 4) {
        pickRhySetting = [...RHYTHM_SETTING['simple']];
    } else if (denominator === 8) {
        if (pickCat.includes("simple")) {
             pickRhySetting = adjustRhythms(RHYTHM_SETTING['simple'], 2);
        } else {
             // Compound time with /8 base (e.g. 6/8)
             pickRhySetting = [...RHYTHM_SETTING['compound']];
        }
    } else if (denominator === 2) {
        // Simple time with /2 base (e.g. 2/2) - half the value (longer notes)
        // Rate = 0.5? 4 -> 2. Yes.
        pickRhySetting = adjustRhythms(RHYTHM_SETTING['simple'], 0.5);
    } else {
        // Fallback
        pickRhySetting = [...RHYTHM_SETTING['simple']];
    }
    
    // Compound with denominator 4 (e.g. 6/4)
    // In Python: elif denominator == Fraction(4, 3) (which comes from 4/3 effectively)
    // 6/4 -> num=2, den=4 (in time sig).
    // Logic: if compound and den=4.
    if (pickCat.includes("compound") && denominator === 4) {
         // adjust_rhythms(compound, 0.5). 4. -> 2.
         pickRhySetting = adjustRhythms(RHYTHM_SETTING['compound'], 0.5);
    }

    return {
        category: pickCat,
        numerator: numerator, // This is "number of beats"
        denominator: denominator,
        rhythmList: pickRhySetting,
        timeSignature: pickTimeSign
    };
}

function rhythmGeneration(rhythmList, numberOfBeats) {
    let melody = [];
    while (melody.length < numberOfBeats) {
        melody.push(rhythmList[Math.floor(Math.random() * rhythmList.length)]);
    }
    return melody;
}

function randomInsertNote(melody) {
    const updatedMelody = [];
    
    for (const note of melody) {
        if (note.includes("tuplet")) {
            const startIdx = note.indexOf("{") + 1;
            const endIdx = note.indexOf("}");
            const content = note.substring(startIdx, endIdx).trim();
            const tupletNotes = content.split(/\s+/);
            
            const updatedTupletNotes = tupletNotes.map(n => {
                const pitch = PITCH_LIST[Math.floor(Math.random() * PITCH_LIST.length)];
                return pitch + n;
            });
            
            updatedMelody.push(`${note.substring(0, startIdx)} ${updatedTupletNotes.join(' ')} ${note.substring(endIdx)}`);
        } else {
            const splitNotes = note.split(/\s+/);
            const updatedNotes = splitNotes.map(n => {
                const pitch = PITCH_LIST[Math.floor(Math.random() * PITCH_LIST.length)];
                return pitch + n;
            });
            updatedMelody.push(updatedNotes.join(' '));
        }
    }
    return updatedMelody;
}

function tranSimpleCompound(melody, setting, passStep = false, seed = 0) {
    const newMelody = [];
    let pass1 = false, pass2 = false, pass3 = false;
    
    if (passStep) {
        if (seed === 0) pass1 = true;
        else if (seed === 1) pass2 = true;
        else if (seed === 2) pass3 = true;
    }

    // Determine direction based on SETTING
    // If setting is "simple...", we are in Simple Time, converting TO Compound.
    // If setting is "compound...", we are in Compound Time, converting TO Simple.
    
    const isSimple = setting.includes("simple");

    if (isSimple) {
        // Simple -> Compound
        for (const note of melody) {
            if (note.includes("tuplet")) {
                // Remove tuplet notation: \tuplet 3/2 {g8 a8 b8} -> g8 a8 b8
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    const content = note.substring(startIdx, endIdx).trim();
                    newMelody.push(content);
                } else {
                    newMelody.push(note);
                }
            } else if (!note.includes(' ')) {
                // Single note: a4 -> a4.
                if (!pass2) {
                    // Extract pitch and duration
                    const match = note.match(/^([a-gA-G][s|f]?)(\d+)(\.*)$/);
                    if (match) {
                        newMelody.push(`${match[1]}${match[2]}.`);
                    } else {
                        newMelody.push(note + "."); // Fallback
                    }
                } else {
                    newMelody.push(note);
                }
            } else {
                // Multi note: g8 a8 -> \tuplet 2/3 { g8 a8 }
                if (!pass3) {
                    newMelody.push(`\\tuplet 2/3 { ${note} }`);
                } else {
                    newMelody.push(note);
                }
            }
        }
    } else {
        // Compound -> Simple
        for (const note of melody) {
            if (note.includes("tuplet")) {
                // Remove tuplet: \tuplet 2/3 { g8 a8 } -> g8 a8
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    const content = note.substring(startIdx, endIdx).trim();
                    newMelody.push(content);
                } else {
                    newMelody.push(note);
                }
            } else if (!note.includes(' ')) {
                // Single dotted note: a4. -> a4
                if (!pass2) {
                    newMelody.push(note.replace('.', ''));
                } else {
                    newMelody.push(note);
                }
            } else {
                // Multi note: g8 a8 b8 -> \tuplet 3/2 { g8 a8 b8 }
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

function correctTranTimeSign(num, den, isToCompound) {
    let newNum = num;
    let newDen = den;
    
    if (isToCompound) {
        newNum = num * 3;
        newDen = den * 2;
    } else {
        newNum = num / 3;
        newDen = den / 2;
    }
    
    return `${newNum}/${newDen}`;
}

function generateQuestionData() {
    const setting = settingGeneration();
    const rhythmMelody = rhythmGeneration(setting.rhythmList, setting.numerator);
    const melody = randomInsertNote(rhythmMelody);
    
    const isSimple = setting.category.includes("simple");
    const targetIsCompound = isSimple;
    
    const [num, den] = setting.timeSignature.split('/').map(Number);
    const correctTimeSig = correctTranTimeSign(num, den, targetIsCompound);
    
    const translatedMelody = tranSimpleCompound(melody, setting.category, false);
    
    const wrongOptions = [];
    const seeds = [0, 1, 2];
    
    seeds.forEach(seed => {
        const wrongMelody = tranSimpleCompound(melody, setting.category, true, seed);
        // Basic check to ensure it's different from correct answer
        if (JSON.stringify(wrongMelody) !== JSON.stringify(translatedMelody)) {
            wrongOptions.push({
                timeSignature: correctTimeSig,
                notes: wrongMelody,
                reason: getReason(seed)
            });
        }
    });
    
    // Fill up to 3 wrong options if duplicates removed
    while (wrongOptions.length < 3) {
         // Generate a random variation if needed, or just duplicate for now
         // Python has elaborate fallback logic, simplified here
         wrongOptions.push({
             timeSignature: correctTimeSig,
             notes: tranSimpleCompound(melody, setting.category, true, Math.floor(Math.random() * 3)),
             reason: "Incorrect modulation"
         });
    }

    const question = {
        timeSignature: setting.timeSignature,
        notes: melody
    };
    
    const answer = {
        timeSignature: correctTimeSig,
        notes: translatedMelody,
        isCorrect: true,
        reason: "Correct translation"
    };
    
    let options = [answer, ...wrongOptions.slice(0, 3)];
    
    // Shuffle options
    options = options.sort(() => Math.random() - 0.5);
    
    const correctIndex = options.findIndex(o => o.isCorrect);
    
    return {
        question,
        options,
        correctIndex
    };
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
