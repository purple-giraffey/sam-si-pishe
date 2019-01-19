import os

def is_vowel(word, pos):
    vowels = ['а', 'е', 'и', 'о', 'у', 'è']
    letter = word[pos]
    if word[pos] in vowels:
        return True
    if letter == 'р' and len(word) > 1:
        if pos == 0 and word[1] not in vowels:
            return True
        if pos > 0 and pos < len(word) - 1 and word[pos-1] not in vowels and word[pos+1] not in vowels:
            return True
        return False
    return False

def count_vowels(word):
    counter = 0
    for i,_ in enumerate(word):
        if is_vowel(word, i):
            counter += 1
    return counter

def find_vowel(syllable):
    for i, _ in enumerate(syllable):
        if is_vowel(syllable, i):
            return syllable[i]

def vowel_extractor(word):
    word_vowels = ""
    for i, letter in enumerate(word):
        if is_vowel(word, i):
            word_vowels += letter
    return word_vowels

def split_word_in_syllables(word):
    word_vowels = []
    vowel_positions = []
    consumed_until_i = -1 # not 0 because it'll ignore the first letter
    for i, letter in enumerate(word):
        if is_vowel(word, i):
            vowel_positions.append(i)
    for vp in vowel_positions:
        word_vowels.append(word[consumed_until_i+1:vp+1]) # from start including the vowel
        consumed_until_i = vp
    if not vowel_positions:
        return [word] # for example, the word 'в' as in 'в кола'
    word_vowels[-1] += word[consumed_until_i+1:len(word)] # rest of last vowel
    return word_vowels

def split_in_syllables(sentence):
    '''
    Returns a list of lists, where each inner list is a word split
    in syllables.
    '''
    syllables = []
    words = sentence.split(' ')
    for word in words:
        syllables.append(split_word_in_syllables(word))
    return syllables

def sounds_similar_syllable(syl1, syl2):
    '''
    Returns a number from 0.0 to 1.0, how similar the syllables sounds.
    '''
    if syl1 == syl2:
        return 1.0
    if find_vowel(syl1) == find_vowel(syl2):
        obezv_syl1 = to_soundless_consonants(syl1)
        obezv_syl2 = to_soundless_consonants(syl2)
        same_letters = 0.0
        for letter in obezv_syl1:
            if letter in obezv_syl2:
                same_letters += 1
        return 0.4 + (same_letters / max(len(syl1), len(syl2))) * 0.5
    return 0.0

def to_soundless_consonants(word):
    '''
    Converts all soundful consonants into soundless (бвгдѓжзѕџ to пфктќшсцч).
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

def tests():
    test_cases = {
        'занимација': [['за', 'ни', 'ма', 'ци', 'ја']],
        'стврднат': [['стврд', 'нат']],
        'брзозборка': [['бр', 'зо', 'збор', 'ка']],
        'звучник на маса': [['звуч', 'ник'], ['на'], ['ма', 'са']],
        'кучката каса': [['куч', 'ка', 'та'], ['ка', 'са']],
        'самовила во бездна': [['са', 'мо', 'ви', 'ла'], ['во'], ['без', 'дна']],
        'тротинетоскопија': [['тро', 'ти', 'не', 'то', 'ско', 'пи', 'ја']],
        'агностицизам': [['аг', 'нос', 'ти', 'ци', 'зам']], # not correct but easier to implement :D
    }

    for sentence in test_cases:
        if split_in_syllables(sentence) != test_cases[sentence]:
            print('It doesnt do anything:', sentence, split_in_syllables(sentence))
        else:
            print('Good!', sentence)

if os.environ.get('RUN_TESTS'):
    tests()