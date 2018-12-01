from find_syllables import split_in_syllables, find_vowel

def obezvuchigi(word):
    '''
    Converts all zvuchni soglaski into bezvuchni.
    '''
    bezvuchen_word = ''
    bezvuchni_counterparts = {}
    for l1, l2 in zip('бвгдѓжзѕџ', 'пфктќшсцч'):
        bezvuchni_counterparts[l1] = l2
    for letter in word:
        if letter in bezvuchni_counterparts:
            bezvuchen_word += bezvuchni_counterparts[letter]
        else:
            bezvuchen_word += letter
    return bezvuchen_word

def flatten(list_of_lists):
    return [y for x in list_of_lists for y in x]

def sounds_similar_syllable(syl1, syl2):
    '''
    Returns a number from 0.0 to 1.0, how similar the syllables sounds.
    '''
    if syl1 == syl2:
        return 1.0
    if find_vowel(syl1) == find_vowel(syl2):
        obezv_syl1 = obezvuchigi(syl1)
        obezv_syl2 = obezvuchigi(syl2)
        same_letters = 0.0
        for letter in obezv_syl1:
            if letter in obezv_syl2:
                same_letters += 1
        return 0.4 + (same_letters / max(len(syl1), len(syl2))) * 0.5
    return 0.0

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


# print(sound_similarity_phrase('те дисам ко на писта', 'ве мислам гомна глиста'))
#print(sound_similarity_phrase('вештина ја најде', 'грешлива на тајмер'))
#print(sound_similarity_phrase('вештина ја најде', 'њук е многу добар'))
#print(sound_similarity_phrase('бараш вештина ја најде', 'кур на главата е рапер'))
#print(sound_similarity_phrase('некој друг е виновен', 'ди нов совет мировен'))
#print(sound_similarity_phrase('пеење', 'пењата'))

#print(split_in_syllables('пеење'))
# print(split_in_syllables('вештина ја најде'))
# print(split_in_syllables('грешлива на тајмер'))