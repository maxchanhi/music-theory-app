
// Convert LilyPond notes to VexFlow keys
// This function replaces image generation with data generation for client-side rendering
function generateQuestionData(chromaticScale, wrongOptions, ascending, clef) {
    let octaveIndex = 4; // Default to C4 (middle C) base
    
    
    let baseOctave = 4; // Treble ascending default
    
    if (clef === "bass") {
        baseOctave = 2; // Bass ascending default (C2)
    } else if (clef === "alto" || clef === "tenor") {
        baseOctave = 3; // Alto/Tenor ascending default (C3)
    } else {
        baseOctave = 4; // Treble ascending default (C4)
    }
    
    if (!ascending) {
        baseOctave += 1; // Start one octave higher for descending
    }

    const correct = convertScaleToVexFlow(chromaticScale, baseOctave);
    const wrongs = wrongOptions.map(opt => convertScaleToVexFlow(opt, baseOctave));
    
    return {
        correct: correct,
        wrongs: wrongs,
        clef: clef
    };
}

function convertScaleToVexFlow(scale, baseOctave) {
    return scale.map(note => {
        // Parse pitch class and octave modifiers
        // Allow 'n' for natural. Note: regex char class [sfn] matches s, f, or n.
        let match = note.match(/^([a-g])([sfn]*)(['|,]*)$/);
        if (!match) return null;
        
        let step = match[1]; // a-g
        let acc = match[2]; // s, f, n, ss, ff
        let octMod = match[3]; // ' or ,
        
        // Convert accidental
        let accidental = "";
        if (acc === "s") accidental = "#";
        else if (acc === "ss") accidental = "##";
        else if (acc === "f") accidental = "b";
        else if (acc === "ff") accidental = "bb";
        else if (acc === "n") accidental = "n"; // Explicit natural
        else if (acc === "fs") accidental = "#"; // Legacy check

        
        // Calculate octave
        let octave = baseOctave;
        if (octMod) {
            for (let char of octMod) {
                if (char === "'") octave++;
                if (char === ",") octave--;
            }
        }
        
        return `${step}${accidental}/${octave}`;
    });
}

module.exports = {
    generateQuestionData
};
