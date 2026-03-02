const Fraction = require('fraction.js');

// Constants
const PITCH_LIST = ["e", "f", "g", "a", "b"];

const RHYTHM_SETTING = {
    "simple": ["4", "8 8", "\\tuplet 3/2 {8 8 8}", "\\tuplet 3/2 {4 8}", "\\tuplet 3/2 {8 4}", "8. 16"],
    "compound": ["4.", "\\tuplet 2/3 {8 8}", "8 8 8", "4 8", "8 4", "\\tuplet 2/3 {8. 16}"]
};

const TIME_SIGN_CAT = {
    "simple duple": [["2/2", 4], ["2/4", 2]],
    "simple triple": [["3/2", 6], ["3/4", 3], ["3/8", 1.5]],
    "simple quadruple": [["4/4", 4], ["4/2", 8]],
    "compound duple": [["6/2", 12], ["6/4", 6], ["6/8", 3], ["6/16", 1.5]],
    "compound triple": [["9/4", 9], ["9/8", 4.5]],
    "compound quadruple": [["12/4", 12], ["12/8", 6]]
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
    while (beat < totalBeat) {
        if (timeSignCat.includes("simple")) {
            const rhythm = RHYTHM_SETTING["simple"][Math.floor(Math.random() * RHYTHM_SETTING["simple"].length)];
            melodyRhythm.push(rhythm);
            beat += 1;
        } else {
            const rhythm = RHYTHM_SETTING["compound"][Math.floor(Math.random() * RHYTHM_SETTING["compound"].length)];
            melodyRhythm.push(rhythm);
            beat += 1.5;
        }
    }

    // Insert pitches
    const melody = randomInsertNote(melodyRhythm);

    // 3. Generate correct answer
    const isSimple = timeSignCat.includes("simple");
    const targetCatPrefix = isSimple ? "compound" : "simple";
    const catType = timeSignCat.split(' ')[1]; // duple, triple, quadruple
    const targetCat = `${targetCatPrefix} ${catType}`;
    
    const targetTimeSignList = TIME_SIGN_CAT[targetCat];
    const targetTimeSignData = targetTimeSignList[Math.floor(Math.random() * targetTimeSignList.length)];
    const correctTimeSig = targetTimeSignData[0];

    const translatedMelody = tranSimpleCompound(melody, timeSignCat, false);

    // 4. Generate wrong options
    const wrongOptions = [];
    const seeds = [0, 1, 2];
    
    seeds.forEach(seed => {
        const wrongMelody = tranSimpleCompound(melody, timeSignCat, true, seed);
        if (JSON.stringify(wrongMelody) !== JSON.stringify(translatedMelody)) {
            wrongOptions.push({
                timeSignature: correctTimeSig,
                notes: wrongMelody,
                reason: getReason(seed)
            });
        }
    });

    while (wrongOptions.length < 3) {
        wrongOptions.push({
            timeSignature: correctTimeSig,
            notes: tranSimpleCompound(melody, timeSignCat, true, Math.floor(Math.random() * 3)),
            reason: "Incorrect modulation"
        });
    }

    const question = {
        timeSignature: timeSignature,
        notes: melody
    };
    
    const answer = {
        timeSignature: correctTimeSig,
        notes: translatedMelody,
        isCorrect: true,
        reason: "Correct translation"
    };
    
    let options = [answer, ...wrongOptions.slice(0, 3)];
    options = options.sort(() => Math.random() - 0.5);
    
    const correctIndex = options.findIndex(o => o.isCorrect);
    
    return {
        question,
        options,
        correctIndex
    };
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
