const Fraction = require('fraction.js');

const pitch_list = ["e", "f", "g", "a", "b"];

const rhythm_setting = {
    "simple": ["4", "8 8", "\\tuplet 3/2 {8 8 8}", "\\tuplet 3/2 {4 8}", "\\tuplet 3/2 {8 4}", "8. 16"],
    "compound": ["4.", "\\tuplet 2/3 {8 8}", "8 8 8", "4 8", "8 4", "\\tuplet 2/3 {8. 16}"]
};

const time_sign_cat = {
    "simple duple": ["2/2", "2/4", "2/8", "2/16"],
    "simple triple": ["3/2", "3/4", "3/8", "3/16"],
    "simple quadruple": ["4/2", "4/4", "4/8", "4/16"],
    "compound duple": ["6/2", "6/4", "6/8", "6/16"],
    "compound triple": ["9/2", "9/4", "9/8", "9/16"],
    "compound quadruple": ["12/2", "12/4", "12/8", "12/16"]
};

const equal_dic = {
    "2,2": [4, 4],
    "3,2": [6, 4],
    "6,8": [3, 4],
    "12,8": [6, 4],
    "2,4": [4, 8]
};

function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function adjustRhythms(rhythms, rate = 2) {
    const adjustedRhythms = [];
    for (let rhythm of rhythms) {
        if (rhythm.includes("tuplet")) {
            const startIdx = rhythm.indexOf("{") + 1;
            const endIdx = rhythm.indexOf("}");
            const tupletNotes = rhythm.substring(startIdx, endIdx).trim().split(/\s+/);
            const adjustedNotes = tupletNotes.map(note => {
                if (note.includes('.')) {
                    const baseDuration = parseInt(note.split('.')[0]) * rate;
                    return `${baseDuration}.`;
                } else {
                    const duration = parseInt(note) * rate;
                    return duration.toString();
                }
            });
            adjustedRhythms.push(`${rhythm.substring(0, startIdx)}${adjustedNotes.join(' ')}${rhythm.substring(endIdx)}`);
        } else {
            const parts = rhythm.trim().split(/\s+/);
            const adjustedParts = parts.map(part => {
                if (part.includes('.')) {
                    const baseDuration = parseInt(part.split('.')[0]) * rate;
                    return `${baseDuration}.`;
                } else {
                    const duration = parseInt(part) * rate;
                    return duration.toString();
                }
            });
            adjustedRhythms.push(adjustedParts.join(' '));
        }
    }
    return adjustedRhythms;
}

function settingGeneration() {
    const categories = Object.keys(time_sign_cat);
    const pickTimeCat = getRandomElement(categories);
    // Pick from index 1 to length-2 (excluding first and last as in Python [1:-1])
    const options = time_sign_cat[pickTimeCat];
    const pickTimeSign = options[Math.floor(Math.random() * (options.length - 2)) + 1];
    
    let [numerator, denominator] = pickTimeSign.split("/").map(Number);
    let pickRhySetting = [];
    let denFrac = new Fraction(denominator);

    if (pickTimeCat.includes("compound")) {
        numerator = numerator / 3;
        denFrac = denFrac.div(3);
    }

    if (denFrac.equals(4)) {
        pickRhySetting = rhythm_setting['simple'];
        denominator = 4;
    } else if (denFrac.equals(8)) {
        pickRhySetting = adjustRhythms(rhythm_setting['simple'], 2);
        denominator = 8;
    } else if (denFrac.equals(new Fraction(8, 3))) {
        pickRhySetting = rhythm_setting['compound'];
        denominator = "8/3";
    } else if (denFrac.equals(new Fraction(4, 3))) {
        pickRhySetting = adjustRhythms(rhythm_setting['compound'], 0.5);
        denominator = "4/3";
    }

    return {
        timeCat: pickTimeCat,
        numerator: Math.floor(numerator),
        denominator: denominator,
        rhythmSetting: pickRhySetting
    };
}

function rhythmGeneration(allRhythmList, numberOfBeat) {
    let melody = [];
    while (melody.length < numberOfBeat) {
        melody.push(getRandomElement(allRhythmList));
    }

    let tupletCheck = false;
    let singleCheck = false;
    let mutiCheck = false;

    for (let note of melody) {
        if (note.includes("tuplet")) {
            tupletCheck = true;
        } else {
            const parts = note.trim().split(/\s+/);
            if (parts.length <= 2) {
                singleCheck = true;
            } else {
                mutiCheck = true;
            }
        }
    }

    if (tupletCheck && (singleCheck || mutiCheck)) {
        return melody;
    } else {
        return rhythmGeneration(allRhythmList, numberOfBeat);
    }
}

function randomInsertNote(melody) {
    return melody.map(note => {
        if (note.includes("tuplet")) {
            const startIdx = note.indexOf("{") + 1;
            const endIdx = note.indexOf("}");
            const tupletNotes = note.substring(startIdx, endIdx).trim().split(/\s+/);
            const updatedTupletNotes = tupletNotes.map(n => getRandomElement(pitch_list) + n);
            return `${note.substring(0, startIdx)}${updatedTupletNotes.join(' ')}${note.substring(endIdx)}`;
        } else {
            const splitNotes = note.trim().split(/\s+/);
            const updatedNotes = splitNotes.map(n => getRandomElement(pitch_list) + n);
            return updatedNotes.join(' ');
        }
    });
}

function tranSimpleCompound(melody = [], setting = "simple", passStep = false, seed = -1) {
    let newMelody = [];
    let pass1 = false, pass2 = false, pass3 = false;
    
    if (passStep) {
        const currentSeed = seed === -1 ? Math.floor(Math.random() * 3) : seed;
        if (currentSeed === 0) pass1 = true;
        else if (currentSeed === 1) pass2 = true;
        else if (currentSeed === 2) pass3 = true;
    }

    if (setting.includes("simple")) { // translate to compound
        for (let note of melody) {
            if (note.includes("tuplet")) {
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    // In Python split("[]") is used, which effectively keeps it as one string if [] is missing
                    const tupletContent = note.substring(startIdx, endIdx).trim();
                    newMelody.push(tupletContent);
                } else {
                    newMelody.push(note);
                }
            } else if (note.length === 2) { // single note e.g. 'a4'
                if (!pass2) {
                    newMelody.push(`${note[0]}${parseInt(note[1])}.`);
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
    } else if (setting.includes("compound")) { // translate to simple
        for (let note of melody) {
            if (note.includes("tuplet")) {
                if (!pass1) {
                    const startIdx = note.indexOf("{") + 1;
                    const endIdx = note.indexOf("}");
                    const tupletNotes = note.substring(startIdx, endIdx).trim().split(/\s+/);
                    newMelody.push(...tupletNotes);
                } else {
                    newMelody.push(note);
                }
            } else if (note.length === 3 && note.endsWith('.')) { // single note e.g. 'a4.'
                if (!pass2) {
                    newMelody.push(`${note[0]}${parseInt(note[1])}`);
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

function correctTranTimeSign(nu, de, switchMode = true) {
    let numerator = nu;
    let denominator = de;

    if (typeof denominator === 'string' && denominator.includes('/')) {
        // Handle Fraction string cases like "8/3"
        if (switchMode) {
            // de * 3/2
            const dFrac = new Fraction(denominator).mul(new Fraction(3, 2));
            denominator = dFrac.valueOf();
        } else {
            // nu * 3, de * 3
            numerator *= 3;
            const dFrac = new Fraction(denominator).mul(3);
            denominator = dFrac.valueOf();
        }
    } else if ([2, 4, 8, 16].includes(Number(denominator))) {
        if (switchMode) {
            numerator *= 3;
            denominator = Number(denominator) * 2;
        }
    }
    return [Math.floor(numerator), Math.floor(denominator)];
}

function removeDuplication(data) {
    const seen = new Set();
    return data.filter(item => {
        const key = `${item[0].join('/')}-${item[1].join(' ')}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });
}

function generateQuestionData() {
    while (true) {
        const { timeCat, numerator, denominator, rhythmSetting } = settingGeneration();
        const rhyMelody = rhythmGeneration(rhythmSetting, numerator);
        const melody = randomInsertNote(rhyMelody);
        
        const timeSign = correctTranTimeSign(numerator, denominator, false);
        const originalMelody = [timeSign, melody];
        
        const translatedTimeSign = correctTranTimeSign(numerator, denominator);
        const translatedMelody = [translatedTimeSign, tranSimpleCompound(melody, timeCat)];
        
        let allOptions = [];
        const reasons = [
            "Failed to remove duplet when compound time modulates to simple time, or vice versa",
            "Failed to identify the value of each beat",
            "Triplet or duplet did not apply during modulation"
        ];

        for (let i = 0; i < 3; i++) {
            const wrongMelodyData = [translatedTimeSign, tranSimpleCompound(melody, timeCat, true, i)];
            if (JSON.stringify(wrongMelodyData) !== JSON.stringify(translatedMelody) && 
                JSON.stringify(wrongMelodyData) !== JSON.stringify(originalMelody)) {
                allOptions.push({
                    value: wrongMelodyData,
                    reason: reasons[i]
                });
            }
        }

        const timeSignKey = `${timeSign[0]},${timeSign[1]}`;
        if (equal_dic[timeSignKey]) {
            const equalTime = equal_dic[timeSignKey];
            const equalTimeMelodyData = [equalTime, translatedMelody[1]];
            const wrongEqualTimeMelodyData = [equalTime, tranSimpleCompound(melody, timeCat, true)];
            
            if (allOptions.length >= 3) {
                allOptions = allOptions.slice(0, 2);
            }
            allOptions.push({
                value: equalTimeMelodyData,
                reason: "Time signature with different value of beat"
            });
            allOptions.push({
                value: wrongEqualTimeMelodyData,
                reason: "Time signature with different value of beat"
            });
        }

        const correctOption = {
            value: translatedMelody,
            reason: "Correct"
        };
        allOptions.push(correctOption);
        
        // Remove duplicates based on value
        const seen = new Set();
        allOptions = allOptions.filter(item => {
            const key = JSON.stringify(item.value);
            if (seen.has(key)) return false;
            seen.add(key);
            return true;
        });

        if (allOptions.length >= 3) {
            // Shuffle options
            for (let i = allOptions.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [allOptions[i], allOptions[j]] = [allOptions[j], allOptions[i]];
            }

            return {
                question: "Which one is the correct metric modulation between simple time and compound time?",
                melody: originalMelody,
                options: allOptions,
                answer: correctOption
            };
        }
    }
}

module.exports = {
    generateQuestionData
};
