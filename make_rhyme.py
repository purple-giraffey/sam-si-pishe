import sys
from os import path
import random

from find_syllables import is_vowel, count_vowels
from rhyme_producer import extract_rhyming_part

with open('zborovi.txt', encoding="utf8") as f:
    list_of_words = f.readlines()

list_of_words = [word.strip() for word in list_of_words]

# todo: rimuvaj so 'r'
# todo: rimuvaj ednoslozhni
# todo: metrika za kvalitet na rimite


def find_rhymes(our_word):
    '''
    Searches through the dictionary for words that rhyme. :D
    '''
    rhymes = []
    print('finding rhymes')
    our_vowel_count = min(count_vowels(our_word), 3)
    our_word_ending = extract_rhyming_part(our_word)
    for dict_word in list_of_words:
        dict_vowel_count = count_vowels(dict_word)
        dict_word_ending = extract_rhyming_part(dict_word)
        if dict_word_ending == our_word_ending and dict_word != our_word:
            if our_vowel_count < 3 and dict_vowel_count > our_vowel_count:
                continue
            rhymes.append(dict_word)
    print('will return rhymes')
    if len(rhymes)>0:
        return rhymes
        #return random.choice(rhymes)

"""if sys.argv[1] == 'еренес':
    print('веренатеренот!')
    exit(0)"""

"""for rhyme in find_rhymes():
    print(rhyme)"""

#print (find_rhymes("хардкоров"))