const path = require('path');

// --- Data ---

const instrumentClef = {
    "flute": "treble clef",
    "piccolo": "treble clef",
    "oboe": "treble clef",
    "cor anglais": "treble clef",
    "clarinet": "treble clef",
    "bassoon": "bass clef or sometimes tenor clef",

    "violin": "treble clef",
    "viola": "alto clef",
    "cello": "bass clef or sometimes tenor clef",
    "double bass": "bass clef",
    "harp": "treble and bass clef/ grand staff",

    "trumpet": "treble clef",
    "horn": "treble clef",
    "trombone": "bass clef or sometimes tenor clef",
    "tuba": "bass clef",
    
    "piano": "treble and bass clef/ grand staff",
    "celesta":"treble and bass clef/ grand staff",
    "timpani": "bass clef",
    "xylophone": "treble clef",
    "marimba": "treble and bass clef/ grand staff",
    "vibraphone": "treble clef",
    "glockenspiel": "treble clef",

    "snare drum/ side drum": "percussion clef (indefinite pitch)",
    "bass drum":"percussion clef (indefinite pitch)",
    "cymbals": "percussion clef (indefinite pitch)",
    "triangle":"percussion clef (indefinite pitch)",
    "tambourine": "percussion clef (indefinite pitch)"
};

const instrumentReeds = {
    "flute": "headjoint (non-reed)",
    "piccolo": "headjoint (non-reed)",
    "oboe": "double reed",
    "cor anglais": "double reed",
    "clarinet": "single reed",
    "bassoon": "double reed",
    "trumpet": "mouthpiece",
    "trombone": "mouthpiece",
    "horn": "mouthpiece",
    "tuba": "mouthpiece"
};

const pianoTerms = {
    "Ped.": "Press the right pedal/ sustain pedal.",
    "con pedale": "Press the right pedal/ sustain pedal.",
    "senza pedale": "Release the right pedal/ sustain pedal.",
    "una corda": "Press the left pedal/ una corda pedal.",
    "tre corda": "Release the left pedal/ una corda pedal.",
    "mano sinistra(m.s.)": "Play with left hand",
    "mano destra(m.d.)": "Play with right hand"
};

const ornamentUrl = {
    "acci_1.jpg": "Acciaccatura",
    "acci_2.jpg": "Acciaccatura",
    "appo_1.jpg": "Appoggiatura",
    // "appo_1.jpg": "Appoggiatura", // Duplicate in Python, skipping
    "ARPEGGIATION_1.jpg": "Appeggiation",
    "ARPEGGIATION_2.jpg": "Appeggiation",
    "mordent_1.jpg": "Mordent",
    "mordent_2.jpg": "Mordent",
    "trill_1.jpg": "Trill",
    "trill_2.jpg": "Trill",
    "turn_1.jpg": "Turn",
    "turn_2.jpg": "Turn",
    "turn_3.jpg": "Turn"
};

const playingTechnique = {
    "strings": ["arco", "pizzicato", "legato", "staccato", "marcato", "accent", "con sordino"],
    "woodwind": ["tonguing", "legato", "staccato", "marcato", "accent"],
    "brass": ["a mute", "tonguing", "legato", "staccato", "marcato", "accent", "con sordino"],
    "indefinite pitch membranophones": ["staccato", "marcato", "accent", "with a mallet/beater"],
    "definite pitch membranophones": ["staccato", "marcato", "accent", "with mallets/beaters", "pitches"],
    "definite pitch ideophones": ["staccato", "marcato", "accent", "with mallets/beaters", "pitches", "chord", "arpeggiation"],
    "indefinite pitch ideophones": ["staccato", "marcato", "accent", "with a mallet/beater", "pitches"],
    "keyboard": ["staccato", "marcato", "accent", "arpeggiation", "with pedal"]
};

const impossibleTechnique = {
    "strings": ["with a mallet/beater", "tonguing", "beater", "pedal"],
    "woodwind": ["with a mallet/beater", "with pedal", "con sordino", "with a mute", "arco", "pizzicato", "chord"],
    "brass": ["with a mallet/beater", "with pedal", "arco", "pizzicato", "chord"],
    "indefinite pitch membranophones": ["arco", "tonguing", "pitches", "arpeggiation"],
    "definite pitch membranophones": ["arco", "tonguing", "pizzicato", "arpeggiation"],
    "definite pitch ideophones": ["a mute", "tonguing", "pizzicato"],
    "indefinite pitch ideophones": ["tonguing", "pizzicato", "arpeggiation", "pitches"],
    "keyboard": ["with a mallet/beater", "arco", "tonguing", "pizzicato"]
};

const instrumentalFamilies = {
    "strings": ["violin", "viola", "cello", "double bass"],
    "woodwind": ["flute", "piccolo", "oboe", "cor anglais", "clarinet", "bassoon"],
    "brass": ["trumpet", "trombone", "horn", "tuba"],
    "keyboard": ["piano", "celesta", "harp"], // harp is not keyboard instrument but shares a lot of tech
    "indefinite pitch membranophones": ["snare drum", "bass drum", "tambourine"],
    "indefinite pitch ideophones": ["cymbals", "triangle"],
    "definite pitch ideophones": ["xylophone", "marimba", "vibraphone", "glockenspiel"],
    "definite pitch membranophones": ["timpani"]
};

const maleVoices = ["Bass", "Baritone", "Tenor"];
const femaleVoices = ["Alto", "Mezzo-soprano", "Soprano"];
const genderLists = [maleVoices, femaleVoices];

// --- Helpers ---

function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function generateOptions(correct, availableOptions) {
    const options = [correct];
    while (options.length < 4) {
        const option = getRandomElement(availableOptions);
        if (!options.includes(option)) {
            options.push(option);
        }
    }
    shuffleArray(options);
    return options;
}

// --- Topic Functions ---

function getReedQuestion() {
    const allReedTypes = ["headjoint (non-reed)", "single reed", "double reed", "mouthpiece"];
    const instrumentKeys = Object.keys(instrumentReeds);
    const instrument = getRandomElement(instrumentKeys);
    const correctReedType = instrumentReeds[instrument];

    const options = [correctReedType];
    while (options.length < 4) {
        const option = getRandomElement(allReedTypes);
        if (!options.includes(option)) {
            options.push(option);
        }
    }
    shuffleArray(options);

    return {
        question: `How does a ${instrument} produce sound?`,
        options: options,
        answer: correctReedType,
        topic: 'Reed'
    };
}

function getTransposingQuestion() {
    const transposingInstruments = ["clarinet", "B-flat trumpet", "horn", "cor anglais"];
    const concertPitchInstruments = ["flute", "oboe", "bassoon", "trombone", "tuba", "violin", "viola", "cello"];
    
    const bothList = [transposingInstruments, concertPitchInstruments];
    const correctList = getRandomElement(bothList);
    const correctAns = getRandomElement(correctList);
    
    const options = [correctAns];
    const falseList = bothList.find(list => list !== correctList);
    
    while (options.length < 4) {
        const option = getRandomElement(falseList);
        if (!options.includes(option)) {
            options.push(option);
        }
    }
    shuffleArray(options);

    let transposingIns = "";
    if (correctList === transposingInstruments) {
        transposingIns = "transposing instrument";
    } else {
        transposingIns = "NOT transposing instrument";
    }

    return {
        question: `Which one is ${transposingIns}?`,
        options: options,
        answer: correctAns,
        topic: 'Transposing'
    };
}

function getClefQuestion() {
    const allClefs = [...new Set(Object.values(instrumentClef))];
    const instrumentKeys = Object.keys(instrumentClef);
    const instrument = getRandomElement(instrumentKeys);
    const useClef = instrumentClef[instrument];
    
    const options = generateOptions(useClef, allClefs);

    return {
        question: `What clef(s) does a ${instrument} use?`,
        options: options,
        answer: useClef,
        topic: 'Clef'
    };
}

function randomPick(lists) {
    const list = getRandomElement(lists);
    return getRandomElement(list);
}

function getVoiceHighLowOptions() {
    const wrongList = [];
    let correctAnswer = null;

    while (wrongList.length < 3 || !correctAnswer) {
        const voice1 = randomPick(genderLists);
        const voice2 = randomPick(genderLists);

        if (voice1 === voice2) continue;

        const statement = `${voice1} is higher than ${voice2}.`;

        // Determine if statement is correct
        let isCorrect = false;

        if (femaleVoices.includes(voice1) && maleVoices.includes(voice2)) {
            isCorrect = true;
        } else if (maleVoices.includes(voice1) && femaleVoices.includes(voice2)) {
            isCorrect = false;
        } else {
            // Same gender list comparison
            const list = maleVoices.includes(voice1) ? maleVoices : femaleVoices;
            const index1 = list.indexOf(voice1);
            const index2 = list.indexOf(voice2);
            // In these lists, higher index means higher pitch?
            // Python: male_voices = ["Bass","Baritone","Tenor"] -> 0=Bass(low), 2=Tenor(high)
            // Python: female_voices = ["Alto","Mezzo-soprano","Soprano"] -> 0=Alto(low), 2=Soprano(high)
            // Python logic: if index_1 > index_2: correct.
            // Yes, standard ordering in arrays above is Low -> High.
            if (index1 > index2) {
                isCorrect = true;
            } else {
                isCorrect = false;
            }
        }

        if (isCorrect) {
            if (!correctAnswer) {
                correctAnswer = statement;
            }
        } else {
            if (!wrongList.includes(statement) && wrongList.length < 3) {
                wrongList.push(statement);
            }
        }
    }

    return { wrongList, correctAnswer };
}

function getVoiceTypesQuestion() {
    // Weighted choice: gender_voice (30%), voice_range (70%)
    const choice = Math.random() < 0.3 ? "gender_voice" : "voice_range";
    
    let options = [];
    let correctAnswer = "";
    let question = "";

    if (choice === "gender_voice") {
        const correctList = getRandomElement(genderLists);
        correctAnswer = getRandomElement(correctList);
        const falseList = genderLists.find(list => list !== correctList);
        
        options = [correctAnswer];
        while (options.length < 4) {
            const option = getRandomElement(falseList);
            if (!options.includes(option)) {
                options.push(option);
            }
        }
        
        const voiceType = (correctList === maleVoices) ? "a male voice type" : "a female voice type";
        question = `Which one is ${voiceType}?`;
        shuffleArray(options);

    } else {
        const result = getVoiceHighLowOptions();
        options = [...result.wrongList, result.correctAnswer];
        correctAnswer = result.correctAnswer;
        question = "Which statement is correct?";
        shuffleArray(options);
    }

    return {
        question: question,
        options: options,
        answer: correctAnswer,
        topic: 'Voice types'
    };
}

function getPianoQuestion() {
    const allKeys = Object.keys(pianoTerms);
    const allOptions = Object.values(pianoTerms);
    
    const correctQuestion = getRandomElement(allKeys);
    const correctAnswer = pianoTerms[correctQuestion];
    
    const options = [correctAnswer];
    while (options.length < 4) {
        const option = getRandomElement(allOptions);
        if (!options.includes(option)) {
            options.push(option);
        }
    }
    shuffleArray(options);

    return {
        question: `What does ${correctQuestion} mean?`,
        options: options,
        answer: correctAnswer,
        topic: 'Piano'
    };
}

function getOrnamentsQuestion() {
    const allUrls = Object.keys(ornamentUrl);
    const allOptionsValues = Object.values(ornamentUrl);
    const uniqueOptions = [...new Set(allOptionsValues)];
    
    const correctQuestionUrl = getRandomElement(allUrls);
    const correctAnswer = ornamentUrl[correctQuestionUrl];
    
    const options = [correctAnswer];
    while (options.length < 4) {
        const option = getRandomElement(uniqueOptions);
        if (!options.includes(option)) {
            options.push(option);
        }
    }
    shuffleArray(options);

    return {
        question: "What is this ornament?",
        pic_url: `/images/instrument_knowledge/${correctQuestionUrl}`,
        options: options,
        answer: correctAnswer,
        topic: 'Ornaments'
    };
}

function getInstrumentalTechniqueQuestion() {
    const allFamilies = Object.keys(playingTechnique);
    const correctFamily = getRandomElement(allFamilies);
    const instrument = getRandomElement(instrumentalFamilies[correctFamily]);
    const thisTechnique = getRandomElement(playingTechnique[correctFamily]);
    
    const correctOption = `A ${instrument} can perform ${thisTechnique}.`;
    
    const options = [];
    // Python code logic: collects 4 wrong options, then adds correct one. Total 5 options.
    while (options.length < 4) {
        const wrongFamily = getRandomElement(allFamilies);
        const wrongInstrument = getRandomElement(instrumentalFamilies[wrongFamily]);
        const wrongTechnique = getRandomElement(impossibleTechnique[wrongFamily]);
        const wrongOption = `A ${wrongInstrument} can perform ${wrongTechnique}.`;
        
        if (!options.includes(wrongOption)) {
            options.push(wrongOption);
        }
    }
    
    options.push(correctOption);
    shuffleArray(options);

    return {
        question: "Which statement is correct?",
        options: options,
        answer: correctOption,
        topic: 'Inst. technique'
    };
}

const topicFunctions = {
    'Reed': getReedQuestion,
    'Transposing': getTransposingQuestion,
    'Clef': getClefQuestion,
    'Voice types': getVoiceTypesQuestion,
    'Piano': getPianoQuestion,
    'Ornaments': getOrnamentsQuestion,
    'Inst. technique': getInstrumentalTechniqueQuestion
};

function getQuestion(selectedTopics) {
    if (!selectedTopics || selectedTopics.length === 0) {
        // Default to all topics if none selected
        selectedTopics = Object.keys(topicFunctions);
    }
    
    // Filter out invalid topics
    const validTopics = selectedTopics.filter(t => topicFunctions[t]);
    if (validTopics.length === 0) return null;

    const chosenTopic = getRandomElement(validTopics);
    return topicFunctions[chosenTopic]();
}

module.exports = {
    getQuestion,
    topics: Object.keys(topicFunctions)
};
