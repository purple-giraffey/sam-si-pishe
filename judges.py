from rhyme_producer import extract_rhyming_part
from find_syllables import count_vowels

class Poem(object):
    def __init__(self, poem_lines=[[]]):
        self.poem_lines = poem_lines
    
    def get_last_line(self):
        return self.poem_lines[-1]
    
    def add_word(self, word):
        last_line = self.get_last_line()
        last_line.append(word)
    
    def press_enter(self):
        self.poem_lines.append([])

def all_lines_rhyming_judge(poem):
    """
    Iterates through lines and checks if the last word rhymes with the last word of the previous line,
    returns a coefficient in range 0-1.
    """
    final_score = 0
    for i, line in enumerate(poem.poem_lines):
        if i == 0:
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
    print (strictness)
    score = 0
    for line in poem.poem_lines:
        line_syllables = sum(count_vowels(word) for word in line)
        print(line_syllables)
        if line_syllables < desired_num_of_syl-strictness or line_syllables > desired_num_of_syl+strictness:
            return 0
            # exit with score 0 even if just one line obviously doesn't match the desired length.
        deviance = abs(desired_num_of_syl - line_syllables)
        print("deviance", deviance)
        score += (strictness - deviance)/strictness
        print("score", score)
    return score/len(poem.poem_lines)
        

example_poem = Poem([
    ['куро', 'ми', 'го', 'јатиш'],
    ['оревче', 'орев', 'клат'],
    ['оревченценценце'],
])

print(example_poem.poem_lines)

print("rhyming judge score", all_lines_rhyming_judge(example_poem))
print("the other judge", syllable_counting_judge(example_poem, 6))

