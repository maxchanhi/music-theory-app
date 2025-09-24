\version "2.24.3"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 4/4
      \omit Score.BarLine
      \tuplet 3/2 {g8 b4} g4 e8. b16 b8 a8
    }
    \layout {
      indent = 0\mm
      ragged-right = ##f
      \context {
        \Score
        \remove "Bar_number_engraver"
      }
    }
}
