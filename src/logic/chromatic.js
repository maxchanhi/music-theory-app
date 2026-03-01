const alphabet = ["c", "d", "e", "f", "g", "a", "b"];
const black_white_key = {
    0: ['c'], 2: ['d'], 4: ['e'],
    5: ['f', 'es'], 7: ['g'], 9: ['a'],
    11: ['b'], 1: ['cs', 'df'], 3: ['ds', 'ef'],
    6: ['fs', 'gf'], 8: ['gs', 'af'], 10: ['as', 'bf']
};

function generateChromaticScale(ascendingDir) {
    const startingPc = Math.floor(Math.random() * 12);
    const startingNote = black_white_key[startingPc][Math.floor(Math.random() * black_white_key[startingPc].length)];

    let chromaticList = [[startingNote]];
    
    if (ascendingDir) {
        return ascending(startingPc, chromaticList);
    } else {
        return descending(startingPc, chromaticList);
    }
}

function descending(startingPc, chromaticList) {
    for (let i = 0; i < 11; i++) {
        let octave = startingPc - i - 1;
        let noteIdx = ((octave % 12) + 12) % 12;
        let noteList = [...black_white_key[noteIdx]];
        if (octave < 0) {
            noteList = noteList.map(el => el + ",");
        }
        chromaticList.push(noteList);
    }

    let chromaticScale = chromaticList.map(note => note[0]);
    chromaticScale.push(chromaticScale[0] + ",");

    for (let i = 2; i < chromaticScale.length; i++) {
        if (chromaticScale[i - 2][0] === chromaticScale[i - 1][0] && chromaticScale[i - 1][0] === chromaticScale[i][0]) {
            let threeSame = chromaticList.slice(i - 2, i + 1);
            for (let idx = 0; idx < threeSame.length; idx++) {
                if (threeSame[idx].length > 1) {
                    chromaticScale[i + idx - 2] = threeSame[idx][1];
                }
            }
        }
    }

    let missingLetter = null;
    for (let letter of alphabet) {
        if (!chromaticScale.join('').includes(letter)) {
            missingLetter = letter;
            break;
        }
    }

    if (missingLetter) {
        let nextNote = alphabet[(alphabet.indexOf(missingLetter) + 1) % alphabet.length];
        for (let i = 0; i < chromaticList.length; i++) {
            for (let el of chromaticList[i]) {
                if (el.includes(missingLetter) && chromaticScale[i + 1] && chromaticScale[i + 1].includes(nextNote)) {
                    chromaticScale[i] = chromaticList[i][1] || chromaticList[i][0];
                    break;
                }
            }
        }
    }

    if (chromaticScale[0].includes("bs")) {
        for (let i = 1; i < chromaticScale.length - 1; i++) {
            chromaticScale[i] = chromaticScale[i].replace(",", "");
        }
        chromaticScale[chromaticScale.length - 1] = "bs,";
    }

    return chromaticScale;
}

function ascending(startingPc, chromaticList) {
    for (let i = 0; i < 11; i++) {
        let octave = startingPc + i + 1;
        let noteIdx = octave % 12;
        let noteList = [...black_white_key[noteIdx]];
        if (octave > 11) {
            noteList = noteList.map(el => el + "'");
        }
        chromaticList.push(noteList);
    }

    let chromaticScale = chromaticList.map(note => note[0]);
    chromaticScale.push(chromaticScale[0] + "'");

    for (let i = 2; i < chromaticScale.length; i++) {
        if (chromaticScale[i - 2][0] === chromaticScale[i - 1][0] && chromaticScale[i - 1][0] === chromaticScale[i][0]) {
            let threeSame = chromaticList.slice(i - 2, i + 1);
            for (let idx = 0; idx < threeSame.length; idx++) {
                if (threeSame[idx].length > 1) {
                    chromaticScale[i + idx - 2] = threeSame[idx][1];
                }
            }
        }
    }

    let missingLetter = null;
    for (let letter of alphabet) {
        if (!chromaticScale.join('').includes(letter)) {
            missingLetter = letter;
            break;
        }
    }

    if (missingLetter) {
        let nextNote = alphabet[(alphabet.indexOf(missingLetter) + 1) % alphabet.length];
        for (let i = 0; i < chromaticList.length; i++) {
            for (let el of chromaticList[i]) {
                if (el.includes(missingLetter) && chromaticScale[i + 1] && chromaticScale[i + 1].includes(nextNote)) {
                    chromaticScale[i] = chromaticList[i][1] || chromaticList[i][0];
                    break;
                }
            }
        }
    }

    if (chromaticScale[0].includes("bs")) {
        chromaticScale[0] = "bs,";
        chromaticScale[chromaticScale.length - 1] = "bs";
    }

    return chromaticScale;
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
