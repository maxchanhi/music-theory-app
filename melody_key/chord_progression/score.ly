
\version "2.22.0"  
\header {
  tagline = "" \language "english"
}

#(set-global-staff-size 26)
\score {

    \fixed c' { 
    \key bf \major

      a8. f16 a8. f16 c16 f16 g16 f16 a4 d4 bf16 bf16 bf16 d16 f8. d16 d4 ef4 ef4 c8. a16 g8. a16 g8. ef16 g8. c16 bf8. f16 bf8. f16
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
      a8. f16 a8. f16 c16 f16 g16 f16 a4 d4 bf16 bf16 bf16 d16 f8. d16 d4 ef4 ef4 c8. a16 g8. a16 g8. ef16 g8. c16 bf8. f16 bf8. f16
      \bar "|"
    }
    \new Staff \fixed c {
      <f a c>1 <bf d f>1 <c ef g>1 <ef g bf>1
      \bar "|"
    }>>
    \midi { }
}
