\version "2.24.1"
\language "english"
\header {
  tagline = ##f
}
\score {
  \new Staff {
    \omit Stem
    \clef "alto"
    \fixed c' {
      \omit TimeSignature
      \omit Score.BarLine
      \omit Score.TimeSignature
      \override Staff.Clef.color = #white
      \override Staff.Clef.layer = #-1
      g fs ef d c bf, a, g,
    }
  }
  \layout {
    indent = 0\mm
  }
}
