
\version "2.24.1"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 3/4
      \omit Score.BarLine
      e4 \tuplet 3/2 {g8 f8 a8} \tuplet 3/2 {e8 f4}
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


