
\version "2.24.1"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)
\score {

    \fixed c' { 
    \key c \major

      c16 c16 d16 c16 f8. c16 f4 a4 g8. a16 b16 b16 g16 e16 g4 g4 e8. b16 g8. e16 g4 e16 a16 c16 a16 g8. f16 b8. g16 b4 b8. d16
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
      c16 c16 d16 c16 f8. c16 f4 a4 g8. a16 b16 b16 g16 e16 g4 g4 e8. b16 g8. e16 g4 e16 a16 c16 a16 g8. f16 b8. g16 b4 b8. d16
      \bar "|"
    }
    \new Staff \fixed c {
      <f a c>1 <g b d>1 <c e g>1 <g b d>1
      \bar "|"
    }>>
    \midi { }
}
