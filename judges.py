from rhyme_producer import extract_rhyming_part
from find_syllables import count_vowels
from pyrsistent import v, pvector, freeze, thaw
from successors_predecessors_client import get_successors
from random import randint

kolede = "коледе леде паднало греде утепало деде деде се мачи баба го квачи за четири јајца гускини шаткини паткини коледе"
vasilica = "македонија кур македонија сакедонија македонија анхедонија македонија наша мила македонија мајка на знаењето"
blaze_it = "везилке кажи како да се роди од ова срце што со себе води проста и строга македонска песна разговор ноќен во тревога бесна два конца парај од срцето драги едниот буди морничави таги едниот црн е а другиот благи другиот копнеж и светол и лаги"

def gen_successors(sentence):
    list_of_words = sentence.split(" ")
    successors = {}
    for i, word in enumerate(list_of_words):
        if i < len(list_of_words)-1:
            if word not in successors:
                successors[word] = [list_of_words[i+1]]
            else:
                successors[word].append(list_of_words[i+1])
    return successors

#successors = gen_successors(blaze_it)

"""successors = {
    "куро" : ["ми", "ти", "мој"],
    "ми" : ["е", "сака", "вози"],
    "клат" : ["е", "твој", "носи"],
    "ти" : ["бидува", "твој", "зема"],
    "мој" : ["мил", "голем", "пенис"]
    }"""

def is_last_line(index, poem_lines):
    return index == 2

def add_word(last_line):
    return last_line.append("bla")

class Poem(object):
    def __init__(self, poem_lines=v(v())):
        self.poem_lines = poem_lines
    
    def add_word(self, word):
        is_last_line = lambda index, poem_lines: index == len(self.poem_lines)-1
        word_appender = lambda last_line: last_line.append(word)
        new_poem_lines = self.poem_lines.transform([is_last_line], word_appender)
        return Poem(new_poem_lines)
    
    def get_last_line(self):
        return self.poem_lines[-1]
    
    def get_last_word(self):
        if len(self.poem_lines[-1]) > 0:
            return self.poem_lines[-1][-1]
        else:
            return self.poem_lines[-2][-1]
    
    def get_last_n_words(self, n=5):
        poem_joined_lines = []
        list_of_poem_lines = thaw(self.poem_lines)
        for line in list_of_poem_lines:
            if len(line) != 0:
                poem_joined_lines.extend(line)
        if len(poem_joined_lines)-1 > n:
            return poem_joined_lines[-n:]
        else:
            return poem_joined_lines
 
    def get_all_last_words(self):
        all_last_words = []
        for line in self.poem_lines:
            if len(line) > 0:
                all_last_words.append(line[-1])
        return all_last_words
    
    def press_enter(self):
        new_poem_lines = self.poem_lines.append(v())
        return Poem(new_poem_lines)

def last_two_lines_rhyming_judge(poem):
    """
    Iterates through lines and checks if the last word rhymes with the last word of the previous line,
    returns a coefficient in range 0-1.
    """
    final_score = 0
    for i, line in enumerate(poem.poem_lines[:-2]):
        if i == 0:
            continue
        if len(line) == 0:
            continue
        last_word = line[-1]
        previous_last_word = poem.poem_lines[i-1][-1]
        if extract_rhyming_part(last_word, 2) == extract_rhyming_part(previous_last_word, 2):
            final_score += 1
    coef = (final_score+1) / len(poem.poem_lines)
    return coef

def syllable_counting_judge(poem, desired_num_of_syl):
    """
    Counts the number of syllables in each line - returns a coefficient.
    """
    strictness = int(desired_num_of_syl/2)
    score = 0
    for line in poem.poem_lines[:-2]:
        line_syllables = sum(count_vowels(word) for word in line)
        if line_syllables < desired_num_of_syl-strictness or line_syllables > desired_num_of_syl+strictness:
            return 0
            # exit with score 0 even if just one line obviously doesn't match the desired length.
        deviance = abs(desired_num_of_syl - line_syllables)
        score += (strictness - deviance)/strictness
    return score/len(poem.poem_lines)

def enter_lover_judge(poem, desired_num_of_syl):
    """
    Loves enters when there isn't a better option.
    """
    last_line = poem.poem_lines[-1]
    line_syllables = sum(count_vowels(word) for word in last_line)
    if line_syllables < desired_num_of_syl:
        return 1
    else:
        return -1*2**(line_syllables-desired_num_of_syl)

def same_ending_hater_judge(poem):
    all_last_words = poem.get_all_last_words()
    unique_last_words = set(all_last_words)
    if len(all_last_words) == len(unique_last_words):
        return 1
    else:
        return -1*2**(len(all_last_words)-len(unique_last_words))

def long_word_lover_judge(poem):
    score = 0
    last_line = poem.get_last_line()
    if len(last_line) == 0:
        return 1
    for word in last_line:
        if len(word) > 2:
            score += 1
    return score/len(last_line)
        
def judges_final_score(poem):
    score = 0
    score += 1000 * last_two_lines_rhyming_judge(poem)
    score += 1000 * syllable_counting_judge(poem, 6)
    score += 20 * enter_lover_judge(poem, 6)
    score += 50 * same_ending_hater_judge(poem)
    score += 100 * long_word_lover_judge(poem)
    score += 10 * randint(-1, 1)
    return score

def gen_possible_moves(poem):
    moves = []
    if len(poem.get_last_line()) != 0:
        moves.append(("press_enter", None))
    last_words = tuple(poem.get_last_n_words(3))
    successors = get_successors(last_words)
    #if last_word in successors:
    for succ in successors:
        moves.append(("add_word", succ))
    return moves

def play_move(poem, move):
    if "add_word" in move:
        return poem.add_word(move[1])
    elif "press_enter" in move:
        return poem.press_enter()

def find_best_move(poem, recursion_level=0):
    possible_moves = gen_possible_moves(poem)
    if not possible_moves:
        return None
    best_score = float("-inf")
    best_move = None
    for move in possible_moves:
        poem_after_move = play_move(poem, move)
        if recursion_level == 6:
            score = judges_final_score(poem_after_move)
        else:
            scored_move = find_best_move(poem_after_move, recursion_level+1)
            if scored_move:
                score = scored_move["score"]
            else:
                score = judges_final_score(poem_after_move)
        if score > best_score:
            best_score = score
            best_move = move
    return {"move": best_move, "score": best_score}

example_poem = Poem(freeze([
    ['куро', 'ми', 'го', 'јатиш'],
    ['оревче', 'орев', 'млат'],
    ['куроти', 'бомбо', 'клат']
]))

example_poem_2 = Poem(freeze([
    ['кога']
]))

for i in range(50):
    next_move = find_best_move(example_poem_2)
    if not next_move:
        break
    example_poem_2 = play_move(example_poem_2, next_move["move"])
    print(next_move, example_poem_2.poem_lines)
    printable_poem = ""
    poem_list = thaw(example_poem_2.poem_lines)
    for line in poem_list:
        printable_poem = printable_poem + "\n" + " ".join(line)
    print (printable_poem)

#print("final judgement", judges_final_score(example_poem))
#print (example_poem.poem_lines)

#print(example_poem.poem_lines.transform([is_last_line], add_word))

#print(example_poem.poem_lines)

#print("rhyming judge score", all_lines_rhyming_judge(example_poem))
#print("the other judge", syllable_counting_judge(example_poem, 6))

