ersion "2.24.3"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    ixed c' {
      	ime 3/4
      \omit Score.BarLine
      \tuplet 3/2 {e4 g8} g8 a8 b8. e16
    }
    \layout {
      indent = 0\mm
      ragged-right = ##f
      \context {
        \Score
        emove "Bar_number_engraver"
      }
    }
}
