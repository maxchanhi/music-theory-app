story_line="""In a colorful animal kingdom, Cleo the cheetah and Ollie the orca were unlikely best friends. One morning, Cleo pinned on her junior ranger BADGE and raced to the seaside CAFE where Ollie lived.

"Let's have an adventure!" Cleo said, her FACE bright with excitement.

They visited Farmer Elephant's CABBAGE patch first. Cleo and Ollie played hide-and-seek among the giant leaves, laughing as the morning began to FADE into afternoon.

Next, they explored the Enchanted Forest. There, they found a magical BAG decorated with BEADED patterns. Inside was an endless supply of treats!

"We can feed all the hungry animals!" Ollie cheered.

On their way home, they met a sad lion cub trapped in a CAGE. Cleo used her speed to find the key, while Ollie kept the cub calm with funny stories. Together, they freed the cub and FED him some treats from their magical bag.

Back at the kingdom, all the animals celebrated Cleo and Ollie's kindness. Their AGED adventure showed that friendship comes in all shapes and sizes, and helping others is the greatest joy of all.
"""

html_upper_pt="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Identify the Notes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }
        h1, h2 {
            color: #333;
        }
        .story {
            margin-bottom: 20px;
        }
        .blank {
            display: inline-block;
            width: 100px;
            border-bottom: 1px solid #000;
            margin: 0 5px;
        }
        input[type="text"] {
            width: 100px;
        }
        .note-image {
            vertical-align: middle;
            margin-right: 1px;
        }
    </style>
</head>
<body>
    <h2>Identify the  Notes</h2>
    <p><strong>Gap-fill exercise</strong></p>
    <p>Fill in all the gaps, then press "Check" to check your answers.</p>
    <div class="story">
        <p>"""
html_lower_pt="""
        </p>
    </div>
    <button onclick="checkAnswers()">Check</button>

    <script>
        function checkAnswers() {
            const inputs = document.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {
                if (input.value.toUpperCase() === input.dataset.answer) {
                    input.style.backgroundColor = 'lightgreen';
                } else {
                    input.style.backgroundColor = 'pink';
                }
            });
        }
    </script>
</body>
</html>
"""

