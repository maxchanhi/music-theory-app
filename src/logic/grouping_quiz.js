const fs = require('fs');
const path = require('path');

const categories = [
    "Correct notation",
    "Dotted rest in simple time",
    "Syncopated rest",
    "Breaking a rest",
    "Beaming issue",
    "Unclear down beat",
    "Hemiola"
];

const folderNames = [
    "Correct_rest",
    "Dotted_rhythm",
    "Syncopated_rest",
    "Breaking_a_rest",
    "beaming",
    "confused_syncopation",
    "hemiola"
];

// Mapping between category names and folder names
const categoryToFolder = categories.reduce((acc, cat, idx) => {
    acc[cat] = folderNames[idx];
    return acc;
}, {});

// Base path for images relative to public directory
// Note: In Node.js environment, we need to handle paths correctly
// The images are in public/images/grouping_quiz
// The logic file is in src/logic
const BASE_IMAGE_PATH = 'images/grouping_quiz';
const PUBLIC_DIR = path.join(__dirname, '../../public');


function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function getQuestion() {
    // 1. Choose a random category
    const chosenCategory = getRandomElement(categories);
    const folderName = categoryToFolder[chosenCategory];
    
    // 2. Get a random image from that category's folder
    const folderPath = path.join(PUBLIC_DIR, BASE_IMAGE_PATH, folderName);
    
    try {
        if (!fs.existsSync(folderPath)) {
            console.error(`Directory not found: ${folderPath}`);
            // Return a default or handle error gracefully
             return null;
        }

        const files = fs.readdirSync(folderPath);
        const imageFiles = files.filter(file => {
            const ext = path.extname(file).toLowerCase();
            return ['.png', '.jpg', '.jpeg'].includes(ext);
        });

        if (imageFiles.length === 0) {
            console.error(`No images found in ${folderPath}`);
            return null;
        }

        const randomImage = getRandomElement(imageFiles);
        // Path relative to public folder for serving
        const imagePath = `/${BASE_IMAGE_PATH}/${folderName}/${randomImage}`;

        return {
            category: chosenCategory,
            imagePath: imagePath
        };

    } catch (error) {
        console.error(`Error generating grouping quiz question: ${error.message}`);
        return null;
    }
}

module.exports = {
    getQuestion,
    categories
};
