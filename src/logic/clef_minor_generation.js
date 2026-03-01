
// Convert LilyPond notes to VexFlow keys for Clef & Minor module
function generateQuestionData(clef, fixedPitch, minorScale) {
    // Determine base octave from fixedPitch (e.g., "c", "c'", "c''", "c,")
    let baseOctave = 4; // Default to c' (C4)
    if (fixedPitch === "c''") baseOctave = 5;
    else if (fixedPitch === "c") baseOctave = 3;
    else if (fixedPitch === "c,") baseOctave = 2;
    
    const vexFlowNotes = minorScale.map(note => {
        // Note can be like "a", "gs", "f'", "c''", "c,"
        let match = note.match(/^([a-g])(s|f|ss|ff)?(['|,]*)$/);
        if (!match) return null;
        
        let step = match[1];
        let acc = match[2] || "";
        let octMod = match[3] || "";
        
        // Convert accidental
        let accidental = "";
        if (acc === "s") accidental = "#";
        else if (acc === "ss") accidental = "##";
        else if (acc === "f") accidental = "b";
        else if (acc === "ff") accidental = "bb";
        
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

    return {
        notes: vexFlowNotes,
        clef: clef
    };
}

module.exports = {
    generateQuestionData
};
