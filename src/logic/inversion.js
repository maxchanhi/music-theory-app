// const { Vex } = require('vexflow'); // VexFlow is client-side only for this app, we don't need it in Node logic for now


// Constants from notation.py
const easymode = ["C major", "A minor", "D major", "B minor", "F major", "D minor", "G major", "E minor",
    "B-flat major", "G minor"];

const intermediate = ["C major", "A minor", "G major", "E minor", "D major", "B minor", "A major", "F-sharp minor",
    "E major", "C-sharp minor", "B major", "G-sharp minor",
    "F major", "D minor", "B-flat major", "G minor", "E-flat major", "C minor",
    "A-flat major", "F minor", "D-flat major", "B-flat minor"];

const funEmojiList = [
    "😂", "🎉", "🚀", "🐱",
    "🐶", "🦄",
    "🎶", "😱", "👼🏻", "💃🏻", "🐰", "🐒", "🐣", "🦀", "💥", "✨", "🥳",
    "🍦", "🌟", "👻",
    "🎈", "🎮", "💩"
];

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

const romanNumerial = ["I", "II", "III", "IV", "V", "VI", "VII"];
const inversionType = ["a", "b", "c"];

// Helper function to get tonal triad
function getTonalTriad(key) {
    const scale = keyscale[key];
    const triadDic = {
        "I": [scale[0], scale[2], scale[4]],
        "II": [scale[1], scale[3], scale[5]],
        "III": [scale[2], scale[4], scale[6]],
        "IV": [scale[3], scale[5], scale[0]],
        "V": [scale[4], scale[6], scale[1]],
        "VI": [scale[5], scale[0], scale[2]],
        "VII": [scale[6], scale[1], scale[3]]
    };
    return triadDic;
}

// Map LilyPond pitch to VexFlow key
// LilyPond: c, d, e, f, g, a, b (middle C is c')
// Our python script uses: c, d, e... and adds ' for octave up, , for octave down
// VexFlow: c/4, d/4, etc.
function mapPitchToVexFlow(pitch) {
    let note = pitch.replace(/['+,]/g, ""); // remove octave markers
    let octave = 4; // default octave (around middle C)
    
    // Count apostrophes for octave up
    const upOctaves = (pitch.match(/'/g) || []).length;
    // Count commas for octave down
    const downOctaves = (pitch.match(/,/g) || []).length;
    
    octave += upOctaves - downOctaves;

    // Handle accidentals
    // Python script uses: s for sharp, f for flat, ss for double sharp
    // VexFlow expects: c#/4, db/4, etc. But for key, it wants c/4 and we add accidental separately
    
    let step = note.charAt(0);
    let accidental = "";
    
    if (note.length > 1) {
        let suffix = note.substring(1);
        if (suffix === "s") accidental = "#";
        else if (suffix === "f") accidental = "b";
        else if (suffix === "ss") accidental = "##";
        else if (suffix === "ff") accidental = "bb";
        else if (suffix === "n") accidental = "n";
        else if (suffix === "gs") accidental = "#"; // Special case from python dict? no, gs is g sharp
    }
    
    return {
        key: `${step}/${octave}`,
        accidental: accidental
    };
}

function generateInversionQuestion(clef = "treble") { // default to treble if not grand/bass
    if (clef === "grand staff") clef = "grand";
    
    const key = easymode[Math.floor(Math.random() * easymode.length)];
    const triadDict = getTonalTriad(key);
    const triadKeys = Object.keys(triadDict);
    
    const pickedTriad = triadKeys[Math.floor(Math.random() * triadKeys.length)];
    // Deep copy to avoid modifying original dictionary
    let triadNotes = [...triadDict[pickedTriad]];
    
    const exceptionPitch = ["a", "b"];
    const inversionKeys = ["a", "b", "c"];
    const inversion = inversionKeys[Math.floor(Math.random() * inversionKeys.length)];
    
    // Inversion logic port from Python
    if (inversion === "a") { // Root position: ['fs', 'a', 'c']
        if (exceptionPitch.includes(triadNotes[0].charAt(0))) {
            triadNotes[1] = triadNotes[1] + "'";
            triadNotes[2] = triadNotes[2] + "'";
        } else if (exceptionPitch.includes(triadNotes[1].charAt(0))) { // c e g
            triadNotes[2] = triadNotes[2] + "'";
        }
    } else if (inversion === "b") { // First inversion
        // Rotate: 1, 2, 0 -> but python does: triad_notes[0], triad_notes[1],triad_notes[2] = triad_notes[1], triad_notes[2], triad_notes[0]
        // [0, 1, 2] -> [1, 2, 0]
        const temp0 = triadNotes[0];
        const temp1 = triadNotes[1];
        const temp2 = triadNotes[2];
        triadNotes[0] = temp1;
        triadNotes[1] = temp2;
        triadNotes[2] = temp0;
        
        if (!exceptionPitch.includes(triadNotes[0].charAt(0))) {
            if (!exceptionPitch.includes(triadNotes[2].charAt(0))) {
                triadNotes[2] = triadNotes[2] + "'";
            } else {
                // pass
            }
        } else if (exceptionPitch.includes(triadNotes[0].charAt(0))) {
            triadNotes[1] = triadNotes[1] + "'";
            triadNotes[2] = triadNotes[2] + "'";
        }
    } else if (inversion === "c") { // Second inversion
        // Rotate: 2, 0, 1 -> Python: triad_notes[0], triad_notes[1], triad_notes[2] = triad_notes[2], triad_notes[0],triad_notes[1]
        // [0, 1, 2] -> [2, 0, 1]
        const temp0 = triadNotes[0];
        const temp1 = triadNotes[1];
        const temp2 = triadNotes[2];
        triadNotes[0] = temp2;
        triadNotes[1] = temp0;
        triadNotes[2] = temp1;
        
        if (!exceptionPitch.includes(triadNotes[0].charAt(0))) {
            if (exceptionPitch.includes(triadNotes[2].charAt(0))) {
                // pass
            } else if (!exceptionPitch.includes(triadNotes[2].charAt(0))) { // e a c
                triadNotes[2] = triadNotes[2] + "'";
                if (!exceptionPitch.includes(triadNotes[1].charAt(0))) {
                    triadNotes[1] = triadNotes[1] + "'";
                }
            }
        } else if (exceptionPitch.includes(triadNotes[0].charAt(0))) { // b e g
            if (!exceptionPitch.includes(triadNotes[2].charAt(0))) {
                triadNotes[2] = triadNotes[2] + "'";
            }
            if (!exceptionPitch.includes(triadNotes[1].charAt(0))) {
                triadNotes[1] = triadNotes[1] + "'";
            }
        }
    }
    
    // Octave adjustment logic
    let adjustNotes = [];
    if (clef === "treble") {
        adjustNotes = [...triadNotes];
    } else if (clef === "bass") {
        // Lower all notes by 2 octaves as requested
        adjustNotes = triadNotes.map(note => note + ",,");
    } else if (clef === "grand") {
        // Ensure 2 notes in bass clef (lowered) and 2 in treble clef (original octave)
        // We take the 3 triad notes, lower the first two for bass
        // Keep the third for treble, and duplicate the first one for treble
        adjustNotes = [];
        adjustNotes.push(triadNotes[0] + ",,"); // Bass
        adjustNotes.push(triadNotes[1] + ",,"); // Bass
        adjustNotes.push(triadNotes[2]);        // Treble
        adjustNotes.push(triadNotes[0]);        // Treble (doubling the lowest note)
    }
    
    // Prepare VexFlow data
    const vexNotes = adjustNotes.map(note => mapPitchToVexFlow(note));
    
    return {
        clef: clef,
        keySign: key,
        triad: pickedTriad,
        inversionType: inversion,
        notes: adjustNotes,
        vexNotes: vexNotes,
        correctAnswer: `${pickedTriad} ${inversion}`
    };
}

module.exports = {
    generateInversionQuestion,
    romanNumerial,
    inversionType,
    funEmojiList
};