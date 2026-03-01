const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const sharp = require('sharp');

const LILYPOND_PATH = 'lilypond'; // Assume lilypond is in PATH
const OUTPUT_DIR = path.join(__dirname, '../../public/images/chromatic');

if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

function generateLilyPondScore(scale, name, clef, octave, ascending) {
    return new Promise((resolve, reject) => {
        const tran = ascending ? 0 : 1;
        const octaveList = ["c,", "c", "c'", "c''"];
        
        // LilyPond content
        let lilypondContent = `\\version "2.22.0"
\\paper {
    left-margin = 10
    right-margin = 10
    top-margin = 10
    bottom-margin = 10
    indent = 0
}
\\layout {
    \\context {
        \\Score
        \\omit BarLine
        \\omit TimeSignature
    }
    \\context {
        \\Staff
        \\remove "Time_signature_engraver"
    }
    ragged-right = ##t
}
#(set-global-staff-size 30)
\\new Staff {
    \\accidentalStyle modern-voice
    \\clef ${clef}
    \\language "english"
    \\fixed ${octaveList[octave + tran]} {
`;

        scale.forEach(pitch => {
            lilypondContent += ` ${pitch}`;
        });

        lilypondContent += `
    }
}
`;

        const lyFilePath = path.join(OUTPUT_DIR, `${name}.ly`);
        fs.writeFileSync(lyFilePath, lilypondContent);

        const lilypondProcess = spawn(LILYPOND_PATH, ['-o', path.join(OUTPUT_DIR, name), '--png', lyFilePath]);

        lilypondProcess.on('close', (code) => {
            if (code === 0) {
                // Crop image
                const pngPath = path.join(OUTPUT_DIR, `${name}.png`);
                cropImage(pngPath).then(resolve).catch(reject);
            } else {
                reject(new Error(`LilyPond exited with code ${code}`));
            }
        });
        
        lilypondProcess.on('error', (err) => {
            reject(err);
        });
    });
}

async function cropImage(imagePath) {
    try {
        const image = sharp(imagePath);
        const metadata = await image.metadata();

        if (!metadata.width || !metadata.height) {
            console.warn("Invalid image metadata for", imagePath);
            return;
        }

        // Extract the top 1/10th of the image first to remove footer text
        // Then trim surrounding whitespace
        // Ensure extract height is at least 1 and does not exceed image height
        const extractHeight = Math.max(1, Math.floor(metadata.height / 9));
        
        if (extractHeight >= metadata.height) {
             const buffer = await image.trim().toBuffer();
             await sharp(buffer).toFile(imagePath);
             return;
        }

        // Step 1: Extract top 1/10th
        let buffer = await image
            .extract({
                left: 0,
                top: 0,
                width: metadata.width,
                height: extractHeight
            })
            .toBuffer();

        // Step 2: Trim whitespace (try-catch separately)
        try {
            buffer = await sharp(buffer).trim().toBuffer();
        } catch (trimErr) {
            console.warn(`Trim failed for ${imagePath}, using extracted image only:`, trimErr.message);
            // If trim fails (e.g. empty image), keep the extracted part
        }
            
        await sharp(buffer).toFile(imagePath); // Overwrite original
    } catch (err) {
        // If overwrite fails (e.g. file busy), we might need a temp file.
        // For now, let's assume it works or log error.
        console.error("Error cropping image:", err);
        // Do not throw, just log, so the app doesn't crash if one image fails
    }
}

async function generateQuestionImages(chromaticScale, wrongOptions, ascending, clef) {
    let octave = 2;
    if (clef === "alto" || clef === "tenor") octave = 1;
    if (clef === "bass") octave = 0;

    const tasks = [];
    
    // Correct answer
    tasks.push(generateLilyPondScore(chromaticScale, "Correct", clef, octave, ascending));
    
    // Wrong options
    wrongOptions.forEach((option, idx) => {
        tasks.push(generateLilyPondScore(option, `wrong_${idx}`, clef, octave, ascending));
    });

    await Promise.all(tasks);
    
    // Return list of generated files
    const files = ["Correct.png"];
    for(let i=0; i<wrongOptions.length; i++) {
        files.push(`wrong_${i}.png`);
    }
    return files;
}

module.exports = {
    generateQuestionImages
};
