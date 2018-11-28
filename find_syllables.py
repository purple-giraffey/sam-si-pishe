import os

vowels = ['а', 'е', 'и', 'о', 'у']

def is_vowel(word, pos):
    letter = word[pos]
    if word[pos] in vowels:
        return True
    if letter == 'р':
        if pos == 0 and word[1] not in vowels:
            return True
        if pos > 0 and pos < len(word) - 1 and word[pos-1] not in vowels and word[pos+1] not in vowels:
            return True
        return False
    return False

def find_vowel(syllable):
    for i, letter in enumerate(syllable):
        if is_vowel(syllable, i):
            return syllable[i]

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