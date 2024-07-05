
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)
\score {

    \fixed c' { 
    \key c \major

      c16 g16 d16 e16 g8. a16 c8. g16 e8 b8 d16 c16 b16 b16 g16 b16 c16 d16 d8 g8 d8. g16 e8. e16 c8. f16 g8. g16 g8 f8 d8. g16 b8. a16 b8. b16 b16 f16 g16 c16
      \bar "|"
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
\score {\new StaffGroup <<
     \new Staff \fixed c' {
      c16 g16 d16 e16 g8. a16 c8. g16 e8 b8 d16 c16 b16 b16 g16 b16 c16 d16 d8 g8 d8. g16 e8. e16 c8. f16 g8. g16 g8 f8 d8. g16 b8. a16 b8. b16 b16 f16 g16 c16
      \bar "|"
    }
    \new Staff \fixed c {
      <c e g>1 <g b d>1 <c e g>1 <g b d>1
      \bar "|"
    }>>
    \midi { }
}
