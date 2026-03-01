const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const sharp = require('sharp');

const OUTPUT_DIR = path.join(__dirname, '../../public/images/clef_minor');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
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
        const extractHeight = Math.max(1, Math.floor(metadata.height / 4));
        
        console.log(`Cropping ${imagePath}: width=${metadata.width}, height=${metadata.height}, extractHeight=${extractHeight}`);

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
        console.error("Error cropping image:", err);
    }
}

function generateLilyPondScore(melody, filename, clef, fixedPitch) {
    return new Promise((resolve, reject) => {
        const lilyString = `\\version "2.24.1"
\\language "english"
\\header {
  tagline = ##f
}
\\score {
  \\new Staff {
    \\omit Stem
    \\clef "${clef}"
    \\fixed ${fixedPitch} {
      \\omit TimeSignature
      \\omit Score.BarLine
      \\omit Score.TimeSignature
      \\override Staff.Clef.color = #white
      \\override Staff.Clef.layer = #-1
      ${melody.join(' ')}
    }
  }
  \\layout {
    indent = 0\\mm
  }
}
`;
        
        const lyPath = path.join(OUTPUT_DIR, `${filename}.ly`);
        const pngPath = path.join(OUTPUT_DIR, `${filename}.png`); // LilyPond adds .png automatically? No, we specify output
        
        fs.writeFileSync(lyPath, lilyString);
        
        // LilyPond output filename handling is tricky. 
        // If we use -o output_base, it generates output_base.png
        
        const lilypondProcess = spawn('lilypond', [
            '--png',
            `-o${path.join(OUTPUT_DIR, filename)}`, // Output base name (without extension)
            lyPath
        ]);
        
        lilypondProcess.stderr.on('data', (data) => {
            // console.log(`LilyPond stderr: ${data}`);
        });
        
        lilypondProcess.on('close', async (code) => {
            if (code === 0) {
                // Determine the actual output file name
                // LilyPond might generate filename.png
                const actualPngPath = path.join(OUTPUT_DIR, `${filename}.png`);
                
                if (fs.existsSync(actualPngPath)) {
                    await cropImage(actualPngPath);
                    resolve(actualPngPath);
                } else {
                    reject(new Error(`LilyPond output file not found: ${actualPngPath}`));
                }
            } else {
                reject(new Error(`LilyPond process exited with code ${code}`));
            }
        });
        
        lilypondProcess.on('error', (err) => {
            reject(err);
        });
    });
}

async function generateQuestionImage(clef, fixedPitch, minorScale) {
    // We generate a single image "score_cm"
    await generateLilyPondScore(minorScale, "score_cm", clef, fixedPitch);
    return "score_cm.png";
}

module.exports = {
    generateQuestionImage
};
