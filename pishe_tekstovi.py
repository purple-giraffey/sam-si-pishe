#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
import re

from find_syllables import split_in_syllables

with open('teksts.txt', 'r', encoding = "utf8") as f:
    tekst = f.read()

def split_in_celini(text):
    text = text.lower()
    break_chars = "!?.,\n;–-…—:"
    ignore_chars = "\"„“”'*%$}{()[]0123456789><«"
    celini = []
    celina = []
    for letter in text:
        if letter in break_chars:
            joined = "".join(celina)
            if joined == '':
                continue
            stripped = joined.strip()
            split = re.split('\s+', stripped)
            celini.append(split)
            celina = []
        elif letter in ignore_chars:
            celina.append(" ")
        else:
            celina.append(letter)
    return celini

def find_successors(celini, max_n=2):
    '''
    Generates Markov chains of length max_n. Returns a dict
    of tupples in which the tupples have length from 1 to max_n.

    If we're going though this word list and i=1:

               current
                  |
        ['this', 'is', 'a', 'chain', 'of', 'words']

    and word_list_len is 6, then the max_possible_n is 4, namely:

    { ('is', 'a', 'chain', 'of'): ['words'] }

    the shortest is:

    { ('is'): ['a'] }

    The calculation for max_possible_n is: len(word_list) - i - 1
    '''
    successors = {}
    for word_list in celini:
        word_list_len = len(word_list)
        for i in range(word_list_len):
            max_possible_n = word_list_len - i - 1
            for n in range(0, min(max_possible_n, max_n)):
                key = tuple(word_list[i:i+n+1])
                val = word_list[i+n+1]
                if key in successors:
                    successors[key].append(val)
                else:
                    successors[key] = [val]
    return successors

def generate_meaningful_wordlist(ending_words_tuple, successors):
    counter = 0 # just in case...
    meaningful_wordlist = list(ending_words_tuple)
    while len(ending_words_tuple) and counter < 1 * 1000 * 1000 and len(meaningful_wordlist) < 100:
        counter += 1
        if ending_words_tuple in successors:
            next_word = random.choice(successors[ending_words_tuple])
            meaningful_wordlist.append(next_word)
            ending_words_tuple = ending_words_tuple[1:] + (next_word,)
        else:
            ending_words_tuple = ending_words_tuple[1:]
    return meaningful_wordlist

celini = split_in_celini(tekst)
celini_slogovi = []
for word_list in celini:
    slogovi = []
    if word_list == ['']:
        continue
    for word in word_list:
        slogovi.extend(split_in_syllables(word)[0])
        slogovi.extend(' ')
    celini_slogovi.append(slogovi)
    slogovi = []

# print(celini_slogovi[:10])
# print(find_successors(celini_slogovi))
successors = find_successors(celini_slogovi)

# successors = find_successors(celini)
# for _ in range(10):
print("".join(generate_meaningful_wordlist(tuple(split_in_syllables("уморен")[0]), successors)))
