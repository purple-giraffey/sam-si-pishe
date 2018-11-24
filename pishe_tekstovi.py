#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os

with open('teksts.txt', 'r', encoding = "utf8") as f:
    tekst = f.read()

def split_in_celini(text):
    text = text.lower()
    break_chars = "!?.,\n;–-"
    ignore_chars = "\"„“”'*%$}{()[]0123456789><"
    celini = []
    celina = []
    for letter in text:
        if letter in break_chars:
            c = "".join(celina).strip().split(" ")
            if c != [''] and c != [' ']:
                celini.append(c)
            celina = []
        elif letter in ignore_chars:
            celina.append(" ")
        else:
            celina.append(letter)
    return celini

"""def find_successors(word_list):
    successors = {}
    for i, word in enumerate(word_list):
        if i == len(word_list)-1:
            break
        elif word in successors:
            successors[word].append(word_list[i+1])
        else:
            successors[word] = [word_list[i+1]]
    return successors"""

def find_successors_advanced(celini):
    successors = {}
    for word_list in celini:
        for i, first in enumerate(word_list):
            if i >= len(word_list)-2:
                break
            second = word_list[i+1]
            succ = word_list[i+2]
            if (first, second) in successors:
                successors[(first, second)].append(succ)
            else:
                successors[(first, second)] = [succ]
    return successors

clean_split_tekst = split_in_celini(tekst)
successors = find_successors_advanced(split_in_celini(tekst))
# predecessors = find_successors_advanced(clean_split_tekst[::-1])

def generate_meaningful_wordlist(first_second, successors, max_length):
    first, second = first_second
    meaningful_wordlist = [first, second]
    for _ in range(max_length-1):
        if first_second in successors:
            next_word = random.choice(successors[first_second])
            meaningful_wordlist.append(next_word)
            first_second = (second, next_word)
        else:
            for (a, b) in successors:
                if a == second:
                    next_word = random.choice(successors[(a, b)])
                    meaningful_wordlist.extend([b, next_word])
                    first_second = (b, next_word)
                    break
    return meaningful_wordlist

#print (generate_meaningful_wordlist(("како", "си"), successors, 8))
