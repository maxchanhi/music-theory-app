const path = require('path');
const registryPath = path.resolve(__dirname, '..', 'src', 'logic', 'registry');
const registry = require(registryPath);

const command = process.argv[2];

function showHelp() {
  console.log(`
Music Theory AI - CLI Tool

Commands:
  node cli/index.js topics                              List all topics
  node cli/index.js generate <topic> [difficulty]        Generate a question
  node cli/index.js check <topic> <questionId> <answer>  Check an answer
  node cli/index.js quiz <topic> [difficulty]            Interactive quiz session
  node cli/index.js voice                                Start voice tutor session
  node cli/index.js help                                 Show this help
`);
}

async function main() {
  switch (command) {
    case 'topics': {
      const topics = registry.listTopics();
      console.log('\nAvailable topics:\n');
      topics.forEach(t => {
        console.log(`  ${t.topic.padEnd(20)} ${t.name}`);
        console.log(`  ${' '.repeat(20)} ${t.description}`);
        if (t.difficultyLevels) {
          console.log(`  ${' '.repeat(20)} Difficulty levels: ${t.difficultyLevels.join(', ')}`);
        }
        console.log();
      });
      break;
    }

    case 'generate': {
      const topic = process.argv[3];
      const difficulty = process.argv[4];

      if (!topic) {
        console.error('Usage: node cli/index.js generate <topic> [difficulty]');
        process.exit(1);
      }

      const options = {};
      if (difficulty) options.difficulty = difficulty;

      try {
        const question = registry.generateQuestion(topic, options);
        console.log(`\n📝 Question [${topic}]:`);
        console.log(`   ${question.questionText}\n`);

        if (question.choices) {
          if (Array.isArray(question.choices)) {
            question.choices.forEach((c, i) => console.log(`   ${i + 1}. ${c}`));
          } else if (typeof question.choices === 'object') {
            // Composite choices (like interval qualities + intervals)
            for (const [key, vals] of Object.entries(question.choices)) {
              console.log(`   ${key}: ${vals.join(', ')}`);
            }
          }
          console.log();
        }

        console.log(`   Answer format: ${question.answerFormat.type}`);
        console.log(`   Question ID: ${question.questionId}`);
      } catch (err) {
        console.error(`Error: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case 'check': {
      const topic = process.argv[3];
      const questionId = process.argv[4];
      const answer = process.argv.slice(5).join(' ');

      if (!topic || !questionId || !answer) {
        console.error('Usage: node cli/index.js check <topic> <questionId> <answer>');
        process.exit(1);
      }

      console.error('Note: check requires questionData. Use interactive quiz mode instead.');
      console.error('Usage: node cli/index.js quiz <topic> [difficulty]');
      break;
    }

    case 'quiz': {
      const topic = process.argv[3];
      const difficulty = process.argv[4];

      if (!topic) {
        console.error('Usage: node cli/index.js quiz <topic> [difficulty]');
        process.exit(1);
      }

      const readline = require('readline');
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });

      const options = {};
      if (difficulty) options.difficulty = difficulty;

      let score = 0;
      let total = 0;

      async function askQuestion() {
        try {
          const question = registry.generateQuestion(topic, options);
          console.log(`\n📝 ${question.questionText}`);

          if (question.choices && Array.isArray(question.choices)) {
            question.choices.forEach((c, i) => console.log(`   ${i}. ${c}`));
          }

          rl.question('\nYour answer: ', (answer) => {
            total++;
            const checkData = question.rawData || question;
            const result = registry.checkAnswer(topic, checkData, answer.trim());
            console.log(result.correct ? '  ✅ Correct!' : `  ❌ ${result.explanation}`);
            if (result.correct) score++;
            console.log(`  Score: ${score}/${total}`);

            setTimeout(askQuestion, 500);
          });
        } catch (err) {
          console.error(`Error: ${err.message}`);
          rl.close();
        }
      }

      console.log(`\n🎵 Music Theory Quiz - ${topic} (${difficulty || 'default'})`);
      console.log('Type your answer and press Enter. Ctrl+C to quit.\n');
      askQuestion();
      break;
    }

    case 'voice': {
      console.log('\n🎤 Voice tutor mode not available in CLI. Use the web interface at /tutor.\n');
      break;
    }

    case 'help':
    default:
      showHelp();
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
