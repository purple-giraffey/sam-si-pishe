from rhyme_producer import extract_rhyming_part
from find_syllables import count_vowels
from pyrsistent import v, pvector, freeze
from successors_predecessors_client import get_successors
from random import randint

kolede = "коледе леде паднало греде утепало деде деде се мачи баба го квачи за четири јајца гускини шаткини паткини коледе"
vasilica = "македонија кур македонија сакедонија македонија анхедонија македонија наша мила македонија мајка на знаењето"

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

"""successors = {
    "куро" : ["ми", "ти", "мој"],
    "ми" : ["е", "сака", "вози"],
    "клат" : ["е", "твој", "носи"]
    }"""

def is_last_line(index, poem_lines):
    print (index, len(poem_lines))
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
        print(self.poem_lines)
        if len(self.poem_lines[-1]) > 0:
            return self.poem_lines[-1][-1]
        else:
            return self.poem_lines[-2][-1]
    
    def get_all_last_words(self):
        all_last_words = []
        for line in self.poem_lines:
            if len(line) > 0:
                all_last_words.append(line[-1])
        return all_last_words
    
    def press_enter(self):
        new_poem_lines = self.poem_lines.append(v())
        return Poem(new_poem_lines)

def all_lines_rhyming_judge(poem):
    """
    Iterates through lines and checks if the last word rhymes with the last word of the previous line,
    returns a coefficient in range 0-1.
    """
    final_score = 0
    for i, line in enumerate(poem.poem_lines):
        if i == 0:
            continue
        if len(line) == 0:
            continue
        last_word = line[-1]
        previous_last_word = poem.poem_lines[i-1][-1]
        if extract_rhyming_part(last_word) == extract_rhyming_part(previous_last_word):
            final_score += 1
    coef = (final_score+1) / len(poem.poem_lines)
    return coef

def syllable_counting_judge(poem, desired_num_of_syl=16):
    """
    Counts the number of syllables in each line - returns a coefficient.
    """
    strictness = int(desired_num_of_syl/4)
    score = 0
    for line in poem.poem_lines:
        line_syllables = sum(count_vowels(word) for word in line)
        if line_syllables < desired_num_of_syl-strictness or line_syllables > desired_num_of_syl+strictness:
            return 0
            # exit with score 0 even if just one line obviously doesn't match the desired length.
        deviance = abs(desired_num_of_syl - line_syllables)
        score += (strictness - deviance)/strictness
    return score/len(poem.poem_lines)

def enter_lover_judge(poem, desired_num_of_syl=16):
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
        
def judges_final_score(poem):
    return 5*all_lines_rhyming_judge(poem) + \
        20*syllable_counting_judge(poem, 10) + \
        10*enter_lover_judge(poem) + \
        10*same_ending_hater_judge(poem) + \
        randint(-5, 5)


def gen_possible_moves(poem):
    moves = []
    if len(poem.get_last_line()) != 0:
        moves.append(("press_enter", None))
    last_word = poem.get_last_word()
    successors = get_successors((last_word, ))
    for succ in successors:
        moves.append(("add_word", succ))
    return moves

example_poem = Poem(freeze([
    ['куро', 'ми', 'го', 'јатиш'],
    ['оревче', 'орев', 'млат'],
    ['куроти', 'бомбо', 'клат']
]))

example_poem_2 = Poem(freeze([
    ['денот']
]))

for i in range(50):
    possible_moves = gen_possible_moves(example_poem_2)
    best_score = float("-inf")
    best_poem = None
    if not possible_moves:
        break
    for move in possible_moves:
        if "add_word" in move:
            new_poem = example_poem_2.add_word(move[1])
        elif "press_enter" in move:
            new_poem = example_poem_2.press_enter()
        score = judges_final_score(new_poem)
        if score > best_score:
            best_score = score
            best_poem = new_poem
    example_poem_2 = best_poem
for line in example_poem_2.poem_lines:
    print (" ".join(line))


#print("final judgement", judges_final_score(example_poem))
#print (example_poem.poem_lines)

#print(example_poem.poem_lines.transform([is_last_line], add_word))

#print(example_poem.poem_lines)

#print("rhyming judge score", all_lines_rhyming_judge(example_poem))
#print("the other judge", syllable_counting_judge(example_poem, 6))

