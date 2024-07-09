
major_scale = {
    'c': ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
    'g': ['g', 'a', 'b', 'c', 'd', 'e', 'fs'],
    'd': ['d', 'e', 'fs', 'g', 'a', 'b', 'cs'],
    'a': ['a', 'b', 'cs', 'd', 'e', 'fs', 'gs'],
    'e': ['e', 'fs', 'gs', 'a', 'b', 'cs', 'ds'],
    'b': ['b', 'cs', 'ds', 'e', 'fs', 'gs', 'as'],
    'fs': ['fs', 'gs', 'as', 'b', 'cs', 'ds', 'es'],
    'f': ['f', 'g', 'a', 'bf', 'c', 'd', 'e'],
    'bf': ['bf', 'c', 'd', 'ef', 'f', 'g', 'a'],
    'ef': ['ef', 'f', 'g', 'af', 'bf', 'c', 'd'],
    'af': ['af', 'bf', 'c', 'df', 'ef', 'f', 'g'],
    'df': ['df', 'ef', 'f', 'gf', 'af', 'bf', 'c'],
    'gf': ['gf', 'af', 'bf', 'cf', 'df', 'ef', 'f']
}

harmonic_ascending = {
    'a': ['a', 'b', 'c', 'd', 'e', 'f', 'gs'],
    'e': ['e', 'fs', 'g', 'a', 'b', 'c', 'ds'],
    'b': ['b', 'cs', 'd', 'e', 'fs', 'g', 'as'],
    'd': ['d', 'e', 'f', 'g', 'a', 'bf', 'cs'],
    'g': ['g', 'a', 'bf', 'c', 'd', 'ef', 'fs'],
    'fs': ['fs', 'gs', 'a', 'b', 'cs', 'd', 'e'],
    'cs': ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b'],
    'c': ['c', 'd', 'ef', 'f', 'g', 'af', 'b'],
    'f': ['f', 'g', 'af', 'bf', 'c', 'df', 'e'],
    'gs': ['gs', 'as', 'b', 'cs', 'ds', 'e', 'fss'],
    'ds': ['ds', 'es', 'fs', 'gs', 'as', 'b', 'css'], 
    'bf': ['bf', 'c', 'df', 'ef', 'f', 'gf', 'a'],
    'ef': ['ef', 'f', 'gf', 'af', 'bf', 'cf', 'd']
}

melodic_minor_scales = {
    'a': ['a', 'b', 'c', 'd', 'e', 'fs', 'gs'] + [ 'g', 'f', 'e', 'd', 'c', 'b'],
    'e': ['e', 'fs', 'g', 'a', 'b', 'cs', 'ds'] + [ 'd', 'c', 'b', 'a', 'g', 'fs'],
    'b': ['b', 'cs', 'd', 'e', 'fs', 'gs', 'as'] + [ 'a', 'g', 'fs', 'e', 'd', 'cs'],
    'd': ['d', 'e', 'f', 'g', 'a', 'b', 'cs'] + [ 'c', 'bf', 'a', 'g', 'f', 'e'],
    'g': ['g', 'a', 'bf', 'c', 'd', 'e', 'fs'] + ['f', 'ef', 'd', 'c', 'bf', 'a'],
    'fs': ['fs', 'gs', 'a', 'b', 'cs', 'ds', 'e'] + [ 'e', 'd', 'cs', 'b', 'a', 'gs'],
    'cs': ['cs', 'ds', 'e', 'fs', 'gs', 'as', 'b'] + [ 'b', 'a', 'gs', 'fs', 'e', 'ds'],
    'c': ['c', 'd', 'ef', 'f', 'g', 'a', 'b'] + [ 'bf', 'af', 'g', 'f', 'ef', 'd'],
    'f': ['f', 'g', 'af', 'bf', 'c', 'd', 'e'] + ['ef', 'df', 'c', 'bf', 'af', 'g'],
    'gs': ['gs', 'as', 'b', 'cs', 'ds', 'es', 'fss'] + [ 'fs', 'e', 'ds', 'cs', 'b', 'as'],
    'ds': ['ds', 'es', 'fs', 'gs', 'as', 'bs', 'css'] + [ 'cs', 'b', 'as', 'gs', 'fs', 'es'],
    'bf': ['bf', 'c', 'df', 'ef', 'f', 'g', 'a'] + ['af', 'gf', 'f', 'ef', 'df', 'c'],
    'ef': ['ef', 'f', 'gf', 'af', 'bf', 'c', 'd'] + ['df', 'cf', 'bf', 'af', 'gf', 'f']
}
