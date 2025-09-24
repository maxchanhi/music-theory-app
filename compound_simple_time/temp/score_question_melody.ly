\version "2.24.3"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 12/8
      \omit Score.BarLine
      g4. f8 g8 f8 a4. \tuplet 2/3 {b8 b8}
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
