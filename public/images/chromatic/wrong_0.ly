\version "2.22.0"
\paper {
    left-margin = 10
    right-margin = 10
    top-margin = 10
    bottom-margin = 10
    indent = 0
}
\layout {
    \context {
        \Score
        \omit BarLine
        \omit TimeSignature
    }
    \context {
        \Staff
        \remove "Time_signature_engraver"
    }
    ragged-right = ##t
}
#(set-global-staff-size 30)
\new Staff {
    \accidentalStyle modern-voice
    \clef treble
    \language "english"
    \fixed c' {
 f fs g gs a as b c' cs' d' d' e' f'
    }
}
