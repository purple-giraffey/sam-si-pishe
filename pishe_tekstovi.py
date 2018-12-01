#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
import re

from find_syllables import split_in_syllables
from soundalike import sound_similarity_phrase
from make_rhyme import find_rhymes
from successors_predecessors_client import get_successors, get_predecessors, get_random_word

def generate_meaningful_wordlist_old(ending_words_tuple, successors, max_len=4):
    counter = 0 # just in case...
    meaningful_wordlist = list(ending_words_tuple)
    while len(ending_words_tuple) and counter < 1 * 1000 * 1000 and len(meaningful_wordlist) < max_len:
        counter += 1
        if ending_words_tuple in successors:
            next_word = random.choice(successors[ending_words_tuple])
            meaningful_wordlist.append(next_word)
            ending_words_tuple = ending_words_tuple + (next_word,)
        else:
            ending_words_tuple = ending_words_tuple[1:]
    return meaningful_wordlist

def generate_meaningful_wordlist(ending_words_tuple, get_succ_or_pred, max_len=6):
    counter = 0 # just in case...
    meaningful_wordlist = list(ending_words_tuple)
    while len(ending_words_tuple) and counter < 1 * 1000 * 1000 and len(meaningful_wordlist) < max_len:
        counter += 1
        found_succ_or_pred = get_succ_or_pred(ending_words_tuple)
        if found_succ_or_pred:
            next_word = random.choice(found_succ_or_pred)
            meaningful_wordlist.append(next_word)
            ending_words_tuple = ending_words_tuple + (next_word,)
        else:
            ending_words_tuple = ending_words_tuple[1:]
    return meaningful_wordlist

def generate_meaningful_string(ending_words_tuple, get_succ_or_pred):
    meaningful_wordlist = generate_meaningful_wordlist(ending_words_tuple, get_succ_or_pred)
    return " ".join(meaningful_wordlist)

"""celini = split_in_celini(tekst)
celini_slogovi = []
for word_list in celini:
    slogovi = []
    if word_list == ['']:
        continue
    for word in word_list:
        slogovi.extend(split_in_syllables(word)[0])
        slogovi.extend(' ')
    celini_slogovi.append(slogovi)
    slogovi = []"""

# print(celini_slogovi[:10])
# print(find_successors(celini_slogovi))
#successors = find_successors(celini, 5)
#predecessors = find_successors([celina[::-1] for celina in celini])


# successors = find_successors(celini)
#for _ in range(10):
    #print(" ".join(generate_meaningful_wordlist(tuple("среќа моја".split(" ")), successors)))

# def find_random_word_tuple(word_tuples_len_one):
#     return random.choice(word_tuples_len_one)

def find_string_that_rhymes_bruteforce(base_string):
    rand_word = get_random_word(from_which="successors")
    best_match = generate_meaningful_string(rand_word, get_successors)
    best_match_coef = sound_similarity_phrase(base_string, best_match)
    first_word_rhymes = find_rhymes(base_string.split(" ")[0])
    for rhyme in first_word_rhymes:
        x = generate_meaningful_string((rhyme,), get_successors)
        print(x)
        #print('base', base_string.split(" "))
        #x = generate_meaningful_string(find_random_word(successors), successors)
        similarity_coef = sound_similarity_phrase(base_string, x)
        if similarity_coef > best_match_coef and similarity_coef != 1.0:
            best_match = x
            best_match_coef = sound_similarity_phrase(base_string, x)
    return base_string, best_match, best_match_coef

def make_poem(get_succ_or_pred):
    """
    Being a poet.
    """
    initial_rhyme = get_random_word(from_which="predecessors")
    list_of_rhymes = [initial_rhyme] + find_rhymes(initial_rhyme)
    lines = []
    print (list_of_rhymes)
    for rhyme in list_of_rhymes:
        line_string_reversed = generate_meaningful_string((rhyme, ), get_succ_or_pred)
        line_list_reversed = line_string_reversed.split(" ")
        if len(line_list_reversed) > 1:
            lines.append(" ".join(line_list_reversed[::-1]))
    return lines

# successors = {}
# predecessors = {}
# counter = 0
# with open('mkwikinohead.txt', 'r', encoding = "utf8") as f:
#     for line in f.readlines():
#         counter += 1
#         if counter % 1000 == 0:
#             print (counter)
#         celini = split_in_celini(line)
#         find_successors(celini, 2, successors)
#         find_successors([celina[::-1] for celina in celini], 2, predecessors)
#         if counter >= 10000:
#             break


#base_string = generate_meaningful_string(find_random_word_tuple(successors), successors)
# base_string = "бараш вештина ја најде"
#print (base_string)
#print (find_string_that_rhymes(base_string))
#for _ in range(100):
#    print (_, generate_meaningful_string(("се", "вклучува"), successors))
#print (find_string_that_rhymes(base_string))
lines = make_poem(get_predecessors)
for line in lines:
    print (line)
# print(get_random_word(from_which="predecessors"))

# print(generate_meaningful_string(('нешто',), get_predecessors))