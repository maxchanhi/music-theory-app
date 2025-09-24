
  \version "2.24.3"  
  \header {}
    tagline = "" 
  
  #(set-global-staff-size 26) 

  \score {
    {
      \clef "treble" 
      \fixed c'' c
      \clef "treble"
      \fixed c'' f
    }
    \layout {
      indent = 0\mm  % Remove indentation to avoid unnecessary space
      line-width = #50  % Adjust line width to fit your content
      ragged-right = ##f  % To avoid ragged right lines
      \context {
        \Score
        \omit TimeSignature
        \remove "Bar_number_engraver"  % Remove bar numbers
      }
    }
  }
  