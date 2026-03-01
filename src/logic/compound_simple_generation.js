const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const sharp = require('sharp');

const execPromise = util.promisify(exec);

const TEMP_DIR = path.join(__dirname, '../../public/images/compound_simple');

if (!fs.existsSync(TEMP_DIR)) {
    fs.mkdirSync(TEMP_DIR, { recursive: true });
}

function formatMelody(melody) {
    return melody.map(note => {
        return note.replace(/'/g, "").replace(/,/g, "").trim();
    }).join(' ');
}

async function cropImage(imagePath) {
    try {
        const image = sharp(imagePath);
        const metadata = await image.metadata();

        if (!metadata.width || !metadata.height) {
            console.warn("Invalid image metadata for", imagePath);
            return;
        }

        // Use trim to remove whitespace
        const buffer = await image.trim().toBuffer();
        await sharp(buffer).toFile(imagePath);
        
    } catch (err) {
        console.error("Error cropping image:", err);
    }
}

async function generateLilyPondScore(melody, filename, upperTime, lowerTime) {
    const lilypondScore = `
\\version "2.22.0"  
\\header {
  tagline = "" \\language "english"
}

#(set-global-staff-size 26)

\\score {
    \\fixed c' {
      \\time ${upperTime}/${lowerTime}
      \\omit Score.BarLine
      ${formatMelody(melody)}
    }
    \\layout {
      indent = 0\\mm
      ragged-right = ##f
      \\context {
        \\Score
        \\remove "Bar_number_engraver"
      }
    }
}
`;

    const lyFilePath = path.join(TEMP_DIR, `${filename}.ly`);
    const pngFilePathBase = path.join(TEMP_DIR, filename); // LilyPond adds extension
    const pngFilePath = `${pngFilePathBase}.png`;

    fs.writeFileSync(lyFilePath, lilypondScore);

    try {
        await execPromise(`lilypond -dpreview -dbackend=eps --png -dresolution=300 --output=${pngFilePathBase} ${lyFilePath}`);
        
        // Check if file exists (LilyPond might add suffix if multiple pages, but here likely one)
        if (fs.existsSync(pngFilePath)) {
            await cropImage(pngFilePath);
        } else {
            console.error(`Generated image not found at ${pngFilePath}`);
        }
    } catch (error) {
        console.error(`Error generating score for ${filename}:`, error);
    }
}

async function generateQuestionImages(questionData) {
    // Question Melody
    const qMelody = questionData.melody[1];
    const qTime = questionData.melody[0];
    await generateLilyPondScore(qMelody, 'question_melody', qTime[0], qTime[1]);

    // Options
    for (let i = 0; i < questionData.options.length; i++) {
        const option = questionData.options[i];
        const optData = option.value || option; // Handle both object and array format
        const optMelody = optData[1];
        const optTime = optData[0];
        await generateLilyPondScore(optMelody, `wr_option_${i}`, optTime[0], optTime[1]);
    }
}

module.exports = {
    generateQuestionImages
};
