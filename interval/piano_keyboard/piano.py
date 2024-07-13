def piano_generation(note=list):
    upper_part="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .piano {
            display: flex;
            justify-content: center;
            padding: 20px;
        }
        .key {
            width: 40px;
            height: 180px;
            border: 1px solid #333;
            background-color: white;
            margin: 0 1px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            font-size: 12px;
            padding-bottom: 10px;
            box-sizing: border-box;
        }
        .black-key {
            width: 24px;
            height: 120px;
            background-color: black;
            color: white;
            margin: 0 -13px;
            z-index: 1;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            font-size: 12px;
            padding-bottom: 10px;
            box-sizing: border-box;
        }
        .key.active, .black-key.active {
            background-color: #a0a0a0;
        }
    </style>
</head>
<body>
    <div class="piano">
        <!-- Keys will be generated here by JavaScript -->
    </div>

    <script>
        const piano = document.querySelector('.piano');
        const notes =""" + str(note) + """;

        for (let octave = 0; octave < 1; octave++) {
            notes.forEach(note => {
                const key = document.createElement('div');
                key.className = note.includes('#') ? 'black-key key' : 'key';
                key.dataset.note = note + octave;
                key.innerText = note;  
                if (note.includes('p')) {
                    key.classList.add('active'); // Add the class 'active'
                    key.innerText = note.replace('p', ''); // Remove 'p' from the note name
                } else {
                    key.innerText = note; // Add note name as inner text
                }

                piano.appendChild(key);
            });
        }
    </script>
</body>
</html>"""
    return upper_part
