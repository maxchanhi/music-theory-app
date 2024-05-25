instrument_clef = {
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
    }
instrument_reeds = {
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
    }

piano={"Ped.":"Press the right pedal/ sustain pedal.",
       "con pedale":"Press the right pedal/ sustain pedal.",
       "senza pedale":"Release the right pedal/ sustain pedal.",
       "una corda":"Press the left pedal/ una corda pedal.",
       "tre corda":"Release the left pedal/ una corda pedal.",
       "mano sinistra(m.s.)":"Play with left hand",
       "mano destra(m.d.)":"Play with right hand"}

orniment_url={"acci_1.jpg":"Acciaccatura","acci_2.jpg":"Acciaccatura",
              "appo_1.jpg":"Appoggiatura","appo_1.jpg":"Appoggiatura",
              "ARPEGGIATION_1.jpg":"Appeggiation","ARPEGGIATION_2.jpg":"Appeggiation",
              "mordent_1.jpg":"Mordent","mordent_2.jpg":"Mordent",
              "trill_1.jpg":"Trill","trill_2.jpg":"Trill",
              "turn_1.jpg":"Turn","turn_2.jpg":"Turn","turn_3.jpg":"Turn"}
### playing techniques
playing_technique = {
    "strings": ["arco", "pizzicato", "legato", "staccato", "marcato", "accent", "con sordino"],
    "woodwind": ["tonguing", "legato", "staccato", "marcato", "accent"],
    "brass": ["a mute", "tonguing", "legato", "staccato", "marcato", "accent", "con sordino"],
    "indefinite pitch membranophones":["staccato", "marcato", "accent", "with a mallet/beater"],
    "definite pitch membranophones":["staccato", "marcato", "accent", "with mallets/beaters","pitches"],
    "definite pitch ideophones":["staccato", "marcato", "accent", "with mallets/beaters","pitches","chord","arpeggiation"],
    "indefinite pitch ideophones":["staccato", "marcato", "accent", "with a mallet/beater","pitches"],
    "keyboard":["staccato", "marcato", "accent", "arpeggiation","with pedal"]
}
impossiable_technique = {"strings":["with a mallet/beater","tonguing", "beater","pedal"],
                        "woodwind":["with a mallet/beater","with pedal", "con sordino","with a mute","arco", "pizzicato","chord"],
                        "brass":["with a mallet/beater","with pedal","arco", "pizzicato","chord"],
                        "indefinite pitch membranophones":["arco","tonguing","pitches","arpeggiation"],
                        "definite pitch membranophones":["arco","tonguing", "pizzicato","arpeggiation"],
                        "definite pitch ideophones":["a mute","tonguing", "pizzicato"],
                        "indefinite pitch ideophones":["tonguing", "pizzicato","arpeggiation","pitches"],
                        "keyboard":["with a mallet/beater","arco","tonguing", "pizzicato"]  }

instrumental_families = {
    "strings": ["violin", "viola", "cello", "double bass"],
    "woodwind": ["flute", "piccolo", "oboe", "cor anglais", "clarinet", "bassoon"],
    "brass": ["trumpet", "trombone", "horn", "tuba"],
    "keyboard": ["piano", "celesta","harp"],#harp is not keyboard instrument but shares a lot of tech
    "indefinite pitch membranophones":["snare drum", "bass drum", "tambourine"],
    "indefinite pitch ideophones":["cymbals", "triangle"],
    "definite pitch ideophones":["xylophone", "marimba", "vibraphone", "glockenspiel"],
    "definite pitch membranophones":["timpani"]
    }


fun_emoji_list = [
    "😂",  # Face with Tears of Joy
    "🎉",  # Party Popper
    "🚀",  # Rocket
    "🐱",  # Cat Face
    "🐶",  # Dog Face
    "🦄",  # Unicorn
    "🎶",  # Musical Notes
    "😱","👼🏻","💃🏻","🐰","🐒","🐣","🦀","💥","✨","🥳",
    "🍦",  # Soft Ice Cream
    "🌟",  # Glowing Star
    "👻",  # Ghost
    "🎈",  # Balloon
    "🎮",  # Video Game
    "💩"
]
