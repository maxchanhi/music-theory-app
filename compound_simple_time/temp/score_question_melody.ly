
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)

\score {
    \fixed c' {
      \time 12/4
      \omit Score.BarLine
      f2. f2 e4 b4 b2 \tuplet 2/3 {g4 e4}
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
