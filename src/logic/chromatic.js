const alphabet = ["c", "d", "e", "f", "g", "a", "b"];
const black_white_key = {
    0: ['c', 'bs'], 1: ['cs', 'df'], 2: ['d', 'css', 'eff'], 3: ['ds', 'ef'],
    4: ['e', 'ff'], 5: ['f', 'es'], 6: ['fs', 'gf'], 7: ['g', 'fss', 'aff'],
    8: ['gs', 'af'], 9: ['a', 'gss', 'bff'], 10: ['as', 'bf'], 11: ['b', 'cf']
};
const getFullSpellings = (() => {
    return (pc, includeTheoretical = false) => {
        return black_white_key[pc] || [];
    };
})();

function generateChromaticScale(ascendingDir) {
    const startingPc = Math.floor(Math.random() * 12);
    const potentialStarts = black_white_key[startingPc];
    const startingPitch = potentialStarts[Math.floor(Math.random() * potentialStarts.length)];

    let scale = [startingPitch];
    let nextNum = startingPc;
    let currentOctaveMod = "";
    const direction = ascendingDir ? 1 : -1;
    // Track letters used so far — ensure every letter (A-G) appears at least once
    const usedLetters = new Set([startingPitch[0]]);
    const letterCount = {};
    letterCount[startingPitch[0]] = 1;

    while (scale.length < 12) {
        const prevNum = nextNum;
        nextNum = (nextNum + direction + 12) % 12;

        // Octave crossing
        if (ascendingDir && nextNum < prevNum) currentOctaveMod += "'";
        else if (!ascendingDir && nextNum > prevNum) currentOctaveMod += ",";

        const potentials = black_white_key[nextNum];
        const prevLetter = scale[scale.length - 1].replace(/['+,]/g, '')[0];

        // Spelling selection rules (priority order):
        // 1. Use a letter not yet used in this scale (ensures all 7 letters appear)
        // 2. Avoid the same letter as the previous note if possible
        // 3. Avoid exceeding 2 occurrences per letter
        // 4. Fall back to any available spelling

        // Check if we still need more letter variety
        const unusedLetters = alphabet.filter(l => !usedLetters.has(l));
        const stillNeedVariety = unusedLetters.length > 0;

            // Score each potential spelling
            const prevBase = scale[scale.length - 1].replace(/['+,]/g, '');
            const prevHasAcc = prevBase.length > 1 && (prevBase.includes('s') || prevBase.includes('f'));
            let best = null, bestScore = -1000;
            for (const p of potentials) {
                let score = 0;
                if (p[0] !== prevLetter) score += 2;        // prefer different letter from previous
                if (!usedLetters.has(p[0])) score += 4;      // strongly prefer unused letters
                if (stillNeedVariety && !usedLetters.has(p[0])) score += 10; // must-pick if still missing letters
                if (prevHasAcc && p[0] === prevBase[0] && p.length === 1) score += 3; // natural resolution after accidental
                // Penalize proportionally to letter count — prevents 3+ occurrences
                score -= (letterCount[p[0]] || 0) * 8;
                if (score > bestScore) { bestScore = score; best = p; }
            }

        let nextPitch = best || potentials[Math.floor(Math.random() * potentials.length)];
        usedLetters.add(nextPitch[0]);
        letterCount[nextPitch[0]] = (letterCount[nextPitch[0]] || 0) + 1;

        // Courtesy natural if same letter as previous with accidental
        if (prevBase[0] === nextPitch[0] && prevHasAcc && nextPitch.length === 1) {
            nextPitch += "n";
        }

        scale.push(nextPitch + currentOctaveMod);
    }

    // Final octave note — add modifier only if the last step crosses an octave
    if (ascendingDir && startingPc < nextNum) currentOctaveMod += "'";
    else if (!ascendingDir && startingPc > nextNum) currentOctaveMod += ",";
    let lastLetter = scale[0];
    const prevBase = scale[scale.length - 1].replace(/['+,]/g, '');
    const prevHasAcc = prevBase.length > 1 && (prevBase.includes('s') || prevBase.includes('f'));
    if (prevBase[0] === scale[0][0] && prevHasAcc && scale[0].length === 1) {
        lastLetter += "n";
    }
    scale.push(lastLetter + currentOctaveMod);

    // Post-process: fix adjacent same-letter issues by respelling enharmonically
    // Build reverse lookup: note base → pc, e.g. "cs" → 1, "df" → 1
    const noteToPc = {};
    for (const [pc, spellings] of Object.entries(black_white_key)) {
        for (const s of spellings) noteToPc[s] = parseInt(pc);
    }
    noteToPc.bs = 0; noteToPc.ff = 4; noteToPc.cf = 11;
    noteToPc.css = 2; noteToPc.eff = 2; noteToPc.fss = 7; noteToPc.aff = 7;
    noteToPc.bff = 9; noteToPc.gss = 9;
    for (let i = 1; i < scale.length; i++) {
        const prev = scale[i-1].replace(/['+,]/g, '');
        const curr = scale[i].replace(/['+,]/g, '');
        if (prev[0] === curr[0]) {
            // Same letter adjacent — count current letter distribution
            const counts = {};
            for (const n of scale) { const l = n.replace(/['+,]/g, '')[0]; counts[l] = (counts[l] || 0) + 1; }
            // Try respelling the CURRENT note
            const pc = noteToPc[curr];
            if (pc !== undefined) {
                const altSpellings = getFullSpellings(pc, true).filter(s => s !== curr && s[0] !== prev[0] && (counts[s[0]] || 0) < 2);
                if (altSpellings.length > 0) {
                    const octMod = scale[i].match(/['+,]*$/)[0];
                    const oldIdx = alphabet.indexOf(curr[0]);
                    const newIdx = alphabet.indexOf(altSpellings[0][0]);
                    const octDiff = -Math.round((newIdx - oldIdx) / 7);
                    let adj = '';
                    if (octDiff > 0) { for (let n = 0; n < octDiff; n++) adj += "'"; }
                    else if (octDiff < 0) { for (let n = 0; n < -octDiff; n++) adj += ","; }
                    scale[i] = altSpellings[0] + octMod + adj;
                } else {
                    // Can't respell current — try respelling PREVIOUS note
                    const prevPc = noteToPc[prev];
                    if (prevPc !== undefined) {
                        const prevAlt = getFullSpellings(prevPc, true).filter(s => s !== prev && s[0] !== curr[0] && (counts[s[0]] || 0) < 2);
                        if (prevAlt.length > 0) {
                            const octMod = scale[i-1].match(/['+,]*$/)[0];
                            const oldIdx = alphabet.indexOf(prev[0]);
                            const newIdx = alphabet.indexOf(prevAlt[0][0]);
                            const octDiff = -Math.round((newIdx - oldIdx) / 7);
                            let adj = '';
                            if (octDiff > 0) { for (let n = 0; n < octDiff; n++) adj += "'"; }
                            else if (octDiff < 0) { for (let n = 0; n < -octDiff; n++) adj += ","; }
                            scale[i-1] = prevAlt[0] + octMod + adj;
                        }
                    }
                }
            }
        }
    }

    // Final safety: ensure first and last note share the same base spelling,
    // then add courtesy natural if the penultimate note has the same letter with accidental
    const lastBase = scale[0].replace(/['+,]*$/, '');
    const lastOct = scale[scale.length - 1].match(/['+,]*$/)[0] || '';
    const penultimate = scale[scale.length - 2].replace(/['+,]/g, '');
    const penHasAcc = penultimate.length > 1 && (penultimate.includes('s') || penultimate.includes('f'));
    const finalBase = (penultimate[0] === lastBase[0] && penHasAcc && lastBase.length === 1) ? lastBase + 'n' : lastBase;
    scale[scale.length - 1] = finalBase + lastOct;

    // Enforce max-2 per letter — run multiple passes with chaining
    for (let pass = 0; pass < 50; pass++) {
        const letterCounts = {};
        for (const n of scale) {
            const l = n.replace(/['+,]/g, '')[0];
            letterCounts[l] = (letterCounts[l] || 0) + 1;
        }
        let changed = false;
        for (const [letter, count] of Object.entries(letterCounts)) {
            if (count <= 2) continue;
            for (let i = 0; i < scale.length; i++) {
                if (letterCounts[letter] <= 2) break;
                if (i === 0 && scale.length > 1) continue; // keep first note spelling
                const base = scale[i].replace(/['+,]/g, '').replace('n', '');
                if (base[0] !== letter) continue;
                const pc = noteToPc[base];
                if (pc === undefined) continue;
                const alt = getFullSpellings(pc, true).filter(s => s !== base && s[0] !== letter);
                if (alt.length === 0) continue;
                // Pick alternative whose target letter has the lowest count (avoid cycles)
                alt.sort((a, b) => (letterCounts[a[0]] || 0) - (letterCounts[b[0]] || 0));
                const octMod = scale[i].match(/['+,]*$/)[0];
                const newL = alt[0][0];
                const oldIdx = alphabet.indexOf(letter);
                const newIdx = alphabet.indexOf(newL);
                const octDiff = -Math.round((newIdx - oldIdx) / 7);
                let adj = '';
                if (octDiff > 0) { for (let n = 0; n < octDiff; n++) adj += "'"; }
                else if (octDiff < 0) { for (let n = 0; n < -octDiff; n++) adj += ','; }
                scale[i] = alt[0] + octMod + adj;
                letterCounts[letter]--;
                letterCounts[newL] = (letterCounts[newL] || 0) + 1;
                changed = true;
            }
        }
        if (!changed) break;
    }
    return scale;
}

function generateWrongOptions(originalScale, ascendingDir) {
    let wrongOptions = [];
    let usedIdx = new Set();
    while (wrongOptions.length < 3) {
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

// Convert LilyPond note string to VexFlow key (e.g. "cs'" → "c#/5")
function lilyToVex(note, clef, ascending) {
    let baseOctave = 4;
    if (clef === 'bass') baseOctave = ascending ? 3 : 4;
    else if (clef === 'alto' || clef === 'tenor') baseOctave = ascending ? 4 : 5;
    else baseOctave = ascending ? 4 : 5; // treble
    const m = note.match(/^([a-g])([sfn]*)(['|,]*)$/);
    if (!m) return 'c/4';
    let step = m[1], acc = m[2] || '', octMod = m[3] || '';
    const accMap = { s: '#', f: 'b', ss: '##', ff: 'bb', n: 'n' };
    let accidental = accMap[acc] || '';
    let octave = baseOctave;
    for (const c of octMod) { if (c === "'") octave++; if (c === ',') octave--; }
    return `${step}${accidental}/${octave}`;
}

function generate(options = {}) {
    const ascending = options.ascending !== undefined ? options.ascending : Math.random() < 0.5;
    const clef = options.clef || (options.clefs?.[0]) || 'treble';

    let chromaticScale, attempts = 0;
    do {
        chromaticScale = generateChromaticScale(ascending);
        attempts++;
        // Verify no letter appears >2 times; retry if invalid
        const cnt = {};
        for (const n of chromaticScale) {
            const l = n.replace(/['+,]/g, '')[0];
            cnt[l] = (cnt[l] || 0) + 1;
        }
        const valid = Object.values(cnt).every(c => c <= 2);
        if (valid) break;
    } while (attempts < 20);

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

    // Convert scales to VexFlow keys for rendering
    const vexOptions = allOptions.map(o => ({
        ...o,
        scale: o.scale.map(n => lilyToVex(n, clef, ascending))
    }));

    return {
        questionText: `Which of these is the correct ${ascending ? 'ascending' : 'descending'} chromatic scale?`,
        answerFormat: { type: 'multiple-choice' },
        choices: allOptions.map(o => o.scale.join(' ')),
        correctAnswer: correctIndex + 1,
        displayData: {
            clef,
            ascending,
            options: vexOptions.map((o, i) => ({
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
    const correct = selectedIdx === questionData.correctAnswer;
    return {
        correct,
        correctAnswer: questionData.correctAnswer,
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

module.exports = { generateChromaticScale, generateWrongOptions, generate, check, meta };
