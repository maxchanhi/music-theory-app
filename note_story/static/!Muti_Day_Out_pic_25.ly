
\version "2.24.3"
\header {
  tagline = ""
}
#(set-global-staff-size 26)

\score {
  \new Staff {
    \clef treble
    \omit Staff.TimeSignature
    \omit Staff.BarLine
    \fixed c' {
    b a' d'' g, e'
    }
  }
  \layout { }
}