const Fraction = require('fraction.js');

const hard_duration = ["hemidemisemiquaver", "demisemiquaver", "semiquaver", "quaver", "crotchet", "minim", "semibreve", "breve"];
const easy_duration = ["semiquaver", "quaver", "crotchet", "minim", "semibreve"];

const duration_fraction = {
    "hemidemisemiquaver": new Fraction(1, 64),
    "demisemiquaver": new Fraction(1, 32),
    "semiquaver": new Fraction(1, 16),
    "quaver": new Fraction(1, 8),
    "crotchet": new Fraction(1, 4),
    "minim": new Fraction(1, 2),
    "semibreve": new Fraction(1),
    "breve": new Fraction(2)
};

const dotted_duration = [new Fraction(1), new Fraction(3, 2), new Fraction(7, 4)];

// Time Signature Logic Constants
const digit_to_rhythm_british = {
    1: "semibreve",
    2: "minim",
    4: "crotchet",
    8: "quaver",
    16: "semiquaver",
    32: "demisemiquaver",
    64: "hemidemisemiquaver"
};

const compound_time_numerator = [6, 9, 12];
const time_denominator = [16, 8, 4, 2];
const denominator_list = [64, 32, 16, 8, 4, 2, 1];
const DOTTED = new Fraction(3, 2);

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateDurationQuestion(options) {
    const { hard, simple, double_dotted } = options;
    
    const durationList = hard ? hard_duration : easy_duration;
    
    let dotted_variation = [" "];
    if (simple) dotted_variation.push("dotted ");
    if (double_dotted) dotted_variation.push("double-dotted ");
    
    const question_idx = getRandomInt(3, durationList.length - 1);
    const question_dur = durationList[question_idx];
    
    const dotted_idx = getRandomInt(0, dotted_variation.length - 1);
    const question_dotted = dotted_variation[dotted_idx];
    const dotted_time = dotted_duration[dotted_idx];
    
    // Ensure small_idx is valid and less than question_idx
    const divisor = getRandomInt(2, 4);
    const small_idx = Math.floor(question_idx / divisor);
    const small_dur = durationList[small_idx];
    
    const big_val = duration_fraction[question_dur].mul(dotted_time);
    const small_val = duration_fraction[small_dur];
    const correctAnswer = big_val.div(small_val).floor().valueOf(); // Using floor division as in Python // operator
    
    return {
        questionText: `How many ${small_dur}s equal to a ${question_dotted}${question_dur}?`,
        correctAnswer: correctAnswer,
        details: {
            small_dur,
            question_dur,
            question_dotted,
            dotted_time_str: dotted_time.toString()
        }
    };
}

function generateTimeSignatureQuestion() {
    const num = compound_time_numerator[Math.floor(Math.random() * compound_time_numerator.length)];
    const den = time_denominator[Math.floor(Math.random() * time_denominator.length)];
    
    const denominator_idx = denominator_list.indexOf(den);
    // In Python code: idx_offset = 1 # random.randint(0, 1) was commented out but set to 1
    const idx_offset = 1; 
    
    // Ensure index is within bounds
    if (denominator_idx + idx_offset >= denominator_list.length) {
        // Fallback if out of bounds (though unlikely with current constants)
        return generateTimeSignatureQuestion();
    }
    
    const small_dur_val = denominator_list[denominator_idx + idx_offset];
    
    // Check if small_dur_val exists in mapping
    if (!digit_to_rhythm_british[small_dur_val]) {
        return generateTimeSignatureQuestion();
    }
    
    const small_dur_name = digit_to_rhythm_british[small_dur_val];
    const questionText = `How many dotted ${small_dur_name}s in ${num}/${den}?`;
    
    const measured_small_dur = DOTTED.mul(new Fraction(1, small_dur_val));
    const full_bar_value = new Fraction(1, den).mul(num);
    const answer = full_bar_value.div(measured_small_dur);
    
    return {
        questionText: questionText,
        correctAnswer: answer.toFraction()
    };
}

function generate(options = {}) {
    const quizType = options.quizType || (Math.random() < 0.5 ? 'duration' : 'time_signature');

    if (quizType === 'time_signature') {
        const q = generateTimeSignatureQuestion();
        return {
            questionText: q.questionText,
            answerFormat: { type: 'free-text' },
            choices: null,
            correctAnswer: q.correctAnswer,
            displayData: null,
            rawData: q
        };
    } else {
        const settings = {
            hard: options.hard || false,
            simple: options.simple !== undefined ? options.simple : true,
            double_dotted: options.double_dotted || false
        };
        const q = generateDurationQuestion(settings);
        return {
            questionText: q.questionText,
            answerFormat: { type: 'free-text' },
            choices: null,
            correctAnswer: String(q.correctAnswer),
            displayData: null,
            rawData: q
        };
    }
}

function check(questionData, userAnswer) {
    const normalized = String(userAnswer).trim();
    const correct = normalized === String(questionData.correctAnswer);

    return {
        correct,
        correctAnswer: String(questionData.correctAnswer),
        explanation: correct
            ? 'Correct! Your duration math is right on pitch.'
            : `The correct answer is ${questionData.correctAnswer}. Remember to use proper note value relationships.`
    };
}

const meta = {
    topic: 'duration_equation',
    name: 'Duration Equations',
    description: 'Calculate note duration equivalencies and time signature math',
    difficultyLevels: null,
    answerType: 'free-text'
};

module.exports = {
    generateDurationQuestion,
    generateTimeSignatureQuestion,
    generate,
    check,
    meta
};
