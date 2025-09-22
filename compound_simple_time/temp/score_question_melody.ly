
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 4/4
      \omit Score.BarLine
      \tuplet 3/2 {e4 e8} e8 a8 \tuplet 3/2 {a8 b4} g4
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
