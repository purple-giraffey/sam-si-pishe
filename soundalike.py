from find_syllables import split_in_syllables, sounds_similar_syllable
from helpers import flatten

def sound_similarity_phrase(phrase1, phrase2):
    '''
    Detects that two phrases sound similar.
    '''
    phrase1_flat = flatten(split_in_syllables(phrase1))
    phrase2_flat = flatten(split_in_syllables(phrase2))
    if len(phrase1_flat) != len(phrase2_flat):
        return 0
    else:
        syllable_similarity_coefs = []
        for syl1, syl2 in zip(phrase1_flat, phrase2_flat):
            syllable_similarity_coefs.append(sounds_similar_syllable(syl1, syl2))
        #print(syllable_similarity_coefs)
        return sum(syllable_similarity_coefs) / len(syllable_similarity_coefs)


#print(sound_similarity_phrase('те дисам ко на писта', 'ве мислам гомна глиста'))
#print(sound_similarity_phrase('вештина ја најде', 'грешлива на тајмер'))
#print(sound_similarity_phrase('вештина ја најде', 'њук е многу добар'))
#print(sound_similarity_phrase('бараш вештина ја најде', 'кур на главата е рапер'))
#print(sound_similarity_phrase('некој друг е виновен', 'ди нов совет мировен'))
#print(sound_similarity_phrase('пеење', 'пењата'))

#print(split_in_syllables('пеење'))
# print(split_in_syllables('вештина ја најде'))
# print(split_in_syllables('грешлива на тајмер'))