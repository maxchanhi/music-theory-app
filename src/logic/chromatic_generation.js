
// Convert LilyPond notes to VexFlow keys
// This function replaces image generation with data generation for client-side rendering
function generateQuestionData(chromaticScale, wrongOptions, ascending, clef) {
    let octaveIndex = 4; // Default to C4 (middle C) base
    
    // Adjust base octave based on clef logic from original code
    // Original: octaveList = ["c,", "c", "c'", "c''"]
    // c, = C2, c = C3, c' = C4 (Middle C), c'' = C5
    // Original logic: octave = 2 for treble -> c' -> C4 base
    // octave = 1 for alto/tenor -> c -> C3 base
    // octave = 0 for bass -> c, -> C2 base
    
    // But wait, the original logic had tran = ascending ? 0 : 1
    // If ascending: tran=0. Treble (octave=2) -> index 2 -> c' -> C4 base
    // If descending: tran=1. Treble (octave=2) -> index 3 -> c'' -> C5 base
    
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
    // scale is array of strings like "c", "cs", "df", "e", "f", "c'"
    // We need to parse each note and apply it relative to baseOctave
    // Since \fixed mode in LilyPond makes notes absolute relative to the fixed pitch,
    // we need to track the "current" octave as we go, or rather, 
    // LilyPond's \fixed mode means "c" is the C immediately above or at the fixed pitch?
    // Actually \fixed c' means "c" is c', "d" is d', "c'" is c'', "c," is c
    // So "c" -> baseOctave
    // "c'" -> baseOctave + 1
    // "c," -> baseOctave - 1
    
    return scale.map(note => {
        // Parse pitch class and octave modifiers
        let match = note.match(/^([a-g])([s|f]*)(['|,]*)$/);
        if (!match) return null;
        
        let step = match[1]; // a-g
        let acc = match[2]; // s (sharp), f (flat), ss, ff, etc.
        let octMod = match[3]; // ' or ,
        
        // Convert accidental
        let accidental = "";
        if (acc === "s") accidental = "#";
        else if (acc === "ss") accidental = "##";
        else if (acc === "f") accidental = "b";
        else if (acc === "ff") accidental = "bb";
        else if (acc === "fs") accidental = "#"; // Typo in original? No, "fs" usually means f-sharp
        // Wait, original logic produced "cs", "df" etc. 
        // Let's assume standard LilyPond: s=sharp, f=flat.
        // Wait, 'es' for E-flat? 'fis' for F-sharp? 
        // The file `src/logic/chromatic.js` uses `black_white_key` with:
        // 1: ['cs', 'df'] -> c-sharp, d-flat
        // So yes, 's' is sharp, 'f' is flat.
        
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
