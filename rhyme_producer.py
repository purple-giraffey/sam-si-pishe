import sys
from os import path
from soundalike import sound_similarity_phrase
from find_syllables import is_vowel, count_vowels, vowel_extractor

#with open('zborovi.txt', encoding="utf8") as f:
    #list_of_words = f.readlines()

#list_of_words = [word.strip() for word in list_of_words]

def extract_rhyming_part(word, up_to_n_vowels=3):
    vowel_count = count_vowels(word)
    counter = max(vowel_count, up_to_n_vowels)
    for i, _ in enumerate(word):
        if is_vowel(word, i):
            if counter == up_to_n_vowels:
                return word[i:]
            counter -= 1
    return word

def rhyming_dict_producer(list_of_words):
    '''
    dict_of_rhymes = {(pt_beyond_vowel):[(word1), (word2), (word3)]}
    ex. dict_of_rhymes = {'ука':['сука', 'брука', 'пука']}
    '''
    dict_of_rhymes = {}
    for word in list_of_words:
        rhyming_part = extract_rhyming_part(word)
        if rhyming_part not in dict_of_rhymes:
            dict_of_rhymes[rhyming_part] = [word]
        else:
            if word not in dict_of_rhymes[rhyming_part]:
                dict_of_rhymes[rhyming_part].append(word)
    return dict_of_rhymes

#dict_of_rhymes = rhyming_dict_producer(list_of_words)

def same_vowels_dict_producer(list_of_words):
    '''
    dict_of_extracted_vowels = {(word_vowels):[(word1), (word2), (word3)]}
    ex. dict_of_extracted_vowels = {'оаиа':['боранија', 'соравија', 'поканива']}
    '''
    dict_of_extracted_vowels = {}
    for word in list_of_words:
        vowels_only = vowel_extractor(word)
        if vowels_only not in dict_of_extracted_vowels:
            dict_of_extracted_vowels[vowels_only] = [word]
        else:
            dict_of_extracted_vowels[vowels_only].append(word)
    return dict_of_extracted_vowels

#extracted_vowels_dict = same_vowels_dict_producer(list_of_words)

def perfect_rhyme_producer(word, dict_of_rhymes):
    # finding perfect rhymes
    word = str(word).lower()
    perfect_rhymes_found = []
    word_rhyming_part = extract_rhyming_part(word)
    if word_rhyming_part in dict_of_rhymes:
        for found_rhyme in dict_of_rhymes[word_rhyming_part]:
            if found_rhyme != word:
                perfect_rhymes_found.append(found_rhyme)
    return perfect_rhymes_found

def rhyme_producer(word, dict_of_rhymes, extracted_vowels_dict):
    '''
    Searches through a dict of word-endings to find a word that rhymes, and returns a dict.
    ex. 'смока' -> {'perfect' : ['стока', 'фока', 'рока',
                    'other' : ['кога', 'рокам', 'мока']
    1. Tries to find a perfect rhyme (two words that have perfectly matching endings)
    from a previously generated dict (ex. тОПКА - кОПКА);
    2. After that: finds similarly sounding words - words with the same vowel structure (ex. кОбИлА - дОпИвА);
    3. For words with more than one syllable: tries to find a rhyme matching max-1 syllables (ex. хипертироидОЗА - бОЗА, сиЛА - маЛА);
    4. If that fails: produces a fail-safe Dzhaka Nakot rhyme (ex. шАРАШ - мАРАШ)
    '''
    word = str(word).lower()
    word_rhyming_part = extract_rhyming_part(word)
    other_rhymes_found = []
    perfect_rhymes_found = perfect_rhyme_producer(word, dict_of_rhymes)
    # 2. finding similarly sounding rhymes based on vowel structure
    extracted_vowels = vowel_extractor(word)
    if extracted_vowels in extracted_vowels_dict:
        other_rhymes_found.extend(extracted_vowels_dict[extracted_vowels])
    # 3. for words with more than 1 syllable - finding rhymes by matching less ending syllables
    if count_vowels(word_rhyming_part) > 1:
        word_rhyming_part_cut = extract_rhyming_part(word_rhyming_part[1:])     
        if word_rhyming_part_cut in dict_of_rhymes:
                other_rhymes_found.extend(dict_of_rhymes[word_rhyming_part_cut])
    # 4. Dzhaka saves the day
    if len(other_rhymes_found) == 0:
        other_rhymes_found.append('м' + word_rhyming_part)
    perfect_rhymes_found = [(rhyme, sound_similarity_phrase(word, rhyme)) for rhyme in perfect_rhymes_found] #if sound_similarity_phrase(word, rhyme) > 0.7]
    other_rhymes_found = [(rhyme, sound_similarity_phrase(word, rhyme)) for rhyme in other_rhymes_found] #if sound_similarity_phrase(word, rhyme) > 0.7]
    all_rhyme_candidates = {'perfect': perfect_rhymes_found, 'other': other_rhymes_found}
    return all_rhyme_candidates

#print (rhyme_producer('краставица', dict_of_rhymes, extracted_vowels_dict))
