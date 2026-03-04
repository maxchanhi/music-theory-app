
// Convert LilyPond notes to VexFlow keys for Clef & Minor module
function generateQuestionData(clef, fixedPitch, minorScale) {
    // VexFlow/LilyPond standard: 'c' is C3 (Small Octave)
    // We ignore fixedPitch for octave calculation because minorScale is now absolute
    const baseOctave = 3; 
    
    const vexFlowNotes = minorScale.map(note => {
        // Note can be like "a", "gs", "f'", "c''", "c,"
        // Regex matches pitch, accidental, and octave modifiers
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
