
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 3/4
      \omit Score.BarLine
      \tuplet 2/3 {a8 a8} b4 \tuplet 3/2 { b4 e8 }
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
