import sys
from os import path

vowels = ['а', 'е', 'и', 'о', 'у']

def is_vowel(word, pos):
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

with open('zborovi.txt', encoding="utf8") as f:
    list_of_words = f.readlines()

list_of_words = [word.strip() for word in list_of_words]

def count_vowels(word):
    counter = 0
    for i,_ in enumerate(word):
        if is_vowel(word, i):
            counter += 1
    return counter

def vowel_extractor(word):
    word_vowels = ""
    for i, letter in enumerate(word):
        if is_vowel(word, i):
            word_vowels += letter
    return word_vowels

def extract_rhyming_part(word):
    '''
    Returns the ending part of the word, starting from the accented vowel (MKD grammar).
    Used for finding perfect rhyme matches.
    '''
    vowel_total = count_vowels(word)
    temp_count = 0
    pt_beyond_vowel = ""
    for i, _ in enumerate(word):
        if is_vowel(word, i):
            temp_count += 1
            if vowel_total == 1 and temp_count == 1:
                pt_beyond_vowel = word[i:]
                break
            elif vowel_total == 2 and temp_count == 1:
                pt_beyond_vowel = word[i:]
                break
            elif vowel_total > 2 and temp_count == vowel_total-2:
                pt_beyond_vowel = word[i:]
                break
    return pt_beyond_vowel

def extract_rhyming_part_last_two_syl(pt_beyond_vowel):
    '''
    Cuts one syllable from the part beyond vowel. Used for finding less sophisticated rhymes
    (ex. придАВКА-чАВКА)
    '''
    temp_count = 0
    pt_beyond_vowel_cut = ""
    for i, _ in enumerate(pt_beyond_vowel):
        if is_vowel(pt_beyond_vowel, i):
            temp_count += 1
            if temp_count == 2:
                pt_beyond_vowel_cut = pt_beyond_vowel[i:]
    return pt_beyond_vowel_cut

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

dict_of_rhymes = rhyming_dict_producer(list_of_words)

def interzvuchigi(word, action):
    '''
    Converts the zvuchni soglaski to bezvuchni or reversed.
    Ozvuchi gi: action = "ozvuchi", obezvuchi gi: action = "obezvuchi"
    '''
    modified_word = ''
    letter_counterparts = {}
    zvuchni = 'бвгдѓжзѕџ'
    bezvuchni = 'пфктќшсцч'
    if action == "ozvuchi":
        for l1, l2 in zip(bezvuchni, zvuchni):
            letter_counterparts[l1] = l2
    elif action == "obezvuchi":
        for l1, l2 in zip(zvuchni, bezvuchni):
            letter_counterparts[l1] = l2
    for letter in word:
        if letter in letter_counterparts:
            modified_word += letter_counterparts[letter]
        else:
            modified_word += letter
    return modified_word

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

extracted_vowels_dict = same_vowels_dict_producer(list_of_words)

def rhyme_producer(word, dict_of_rhymes, extracted_vowels_dict):
    '''
    Searches through a dict of word-endings to find a word that rhymes, and returns a dict.
    ex. 'смока' -> {'perfect' : ['стока', 'фока', 'рока',
                    'other' : ['кога', 'рокам', 'мока']
    1. Tries to find a perfect rhyme (two words that have perfectly matching endings)
    from a previously generated dict (ex. тОПКА - кОПКА);
    2. After that: uses an "interzvuchigi" function to find words with similar endings (ex. тОПОВИ - рОБОВИ);
    3. After that: finds similarly sounding words - words with the same vowel structure (ex. кОбИлА - дОпИвА);
    4. For words with more than one syllable: tries to find a rhyme matching max-1 syllables (ex. хипертироидОЗА - бОЗА, сиЛА - маЛА);
    5. If that fails: produces a fail-safe Dzhaka Nakot rhyme (ex. шАРАШ - мАРАШ)
    '''
    word = str(word).lower()
    word_rhyming_part = extract_rhyming_part(word)
    perfect_rhymes_found = []
    other_rhymes_found = []
    # 1. finding perfect rhymes
    if word_rhyming_part in dict_of_rhymes:
        for found_rhyme in dict_of_rhymes[word_rhyming_part]:
            if found_rhyme != word:
                perfect_rhymes_found.append(found_rhyme)
    # 2. finding rhymes based on interzvuchuvanje
    ozvuchen_word_part = interzvuchigi(word_rhyming_part, "ozvuchi")
    obezvuchen_word_part = interzvuchigi(word_rhyming_part, "obezvuchi")
    if ozvuchen_word_part != word_rhyming_part and ozvuchen_word_part in dict_of_rhymes:
        other_rhymes_found.append(dict_of_rhymes[ozvuchen_word_part])
    if obezvuchen_word_part != word_rhyming_part and obezvuchen_word_part in dict_of_rhymes:
        other_rhymes_found.append(dict_of_rhymes[obezvuchen_word_part])
    # 3. finding similarly sounding rhymes based on consonant structure
    extracted_vowels = vowel_extractor(word)
    if extracted_vowels in extracted_vowels_dict:
        other_rhymes_found.append(extracted_vowels_dict[extracted_vowels])
    # 4. for words with more than 1 syllable - finding rhymes by matching less ending syllables
    if count_vowels(word_rhyming_part) > 1:
        word_rhyming_part_cut = extract_rhyming_part_last_two_syl(word_rhyming_part)     
        if word_rhyming_part_cut in dict_of_rhymes:
                other_rhymes_found.append(dict_of_rhymes[word_rhyming_part_cut])
    # 5. Dzhaka saves the day
    if len(other_rhymes_found) == 0:
        other_rhymes_found.append('м' + word_rhyming_part)
    all_rhyme_candidates = {'perfect': perfect_rhymes_found, 'other': other_rhymes_found}
    return all_rhyme_candidates

print (rhyme_producer('потполошка', dict_of_rhymes, extracted_vowels_dict))
