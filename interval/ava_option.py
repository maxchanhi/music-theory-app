
all_quality= ['Diminished', 'Minor', 'Perfect', 'Major', 'Augmented']
without_perfect = ['Minor',"Major"]
without_mima = ['Perfect']

all_interval=['Unison', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh',
  'Octave', 'Ninth', 'Tenth', 'Eleventh', 'Twelfth', 'Thirteenth', 
  'Fourteenth', 'Compound Octave']
interval_without_mima = ['Unison', 'Fourth', 'Fifth',
  'Octave',  'Eleventh', 'Twelfth', 'Compound Octave']
interval_without_perfect = [ 'Second', 'Third', 'Sixth', 'Seventh',
  'Ninth', 'Tenth', 'Thirteenth', 
  'Fourteenth']

def quality_selection_callback(pick_op):
    if pick_op in without_perfect:
        return interval_without_perfect
    elif pick_op in without_mima:
        return interval_without_mima
    else:
        return all_interval
def interval_selection_callback(pick_op):
    if pick_op in interval_without_mima:
        quality = without_mima
        return ['Diminished']+quality+['Augmented']
    elif pick_op in interval_without_perfect:
        quality = without_perfect
        return ['Diminished']+quality+['Augmented']
    else:
        return all_quality
