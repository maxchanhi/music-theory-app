
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 4/2
      \omit Score.BarLine
      f2 \tuplet 3/2 { f2 e4 } \tuplet 3/2 { b4 b2 } g4 e4
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
