import socket
import json
import traceback

from json_server_client import JsonServer

class RPC(object):
    def __init__(self, service):
        self.service = service
        self.json_server = JsonServer(self.call_method)

    def call_method(self, json_msg):
        if not "method" in json_msg:
            raise Exception("Param 'method' not found")
        if not "params" in json_msg:
            raise Exception("Missing params object")
        method = json_msg["method"]
        params = json_msg["params"]
        try:
            return getattr(self.service, method)(params)
        except:
            print("Error when trying to call service method '%s' with params '%s'" % (method, params))
            traceback.print_exc()

    def listen(self, port):
        self.json_server.listen(port)

###
# Copied from the old server
###

import re
import json
import random
import os

class CorpusService(object):
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.successors = {}
        self.predecessors = {}
        self.successor_word_len_one = self.find_word_tuples_len_one(self.successors)
        self.predecessor_word_len_one = self.find_word_tuples_len_one(self.predecessors)

        counter = 0
        with open(os.path.join(script_dir, 'mk-books-text.txt'), 'r', encoding = "utf8") as f:
            for line in f.readlines():
                counter += 1
                if counter % 1000 == 0:
                    print (counter)
                celini = self.split_in_celini(line)
                self.find_successors(celini, 5, self.successors)
                self.find_successors([celina[::-1] for celina in celini], 5, self.predecessors)
                # if counter >= 100000:
                #     break
    
    def split_in_celini(self, text):
        text = text.lower()
        break_chars = "!?.\n;–-…—:"
        ignore_chars = "\"„“”'*%$}{()[]0123456789><«+=,"
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

    def find_successors(self, celini, max_n=5, successors = {}):
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
        for word_list in celini:
            word_list_len = len(word_list)
            for i in range(word_list_len):
                max_possible_n = word_list_len - i - 1
                for n in range(0, min(max_possible_n, max_n)):
                    key = tuple(word_list[i:i+n+1])
                    val = word_list[i+n+1]
                    if key in successors and val not in successors[key]:
                        successors[key].append(val)
                    else:
                        successors[key] = [val]

    def find_word_tuples_len_one(self, successors):
        word_tuples_len_one = []
        for key in successors:
            if len(key) == 1:
                word_tuples_len_one.append(key)
        return word_tuples_len_one

    def find_random_word_tuple(self, word_tuples_len_one):
        return random.choice(word_tuples_len_one)


    ## Available on the network:

    def get_successors(self, params):
        words_tuple = tuple(params["words"])
        if words_tuple in self.successors:
            return self.successors[words_tuple]
        else:
            return []

    def get_predecessors(self, params):
        words_tuple = tuple(params["words"])
        if words_tuple in self.predecessors:
            return self.predecessors[words_tuple]
        else:
            return []

    def get_random_word_tuple(self, params):
        from_which = params["from_which"]
        return self.find_random_word_tuple(successor_word_len_one if from_which == "successors" else predecessor_word_len_one)

corpus_service = CorpusService()
rpc = RPC(corpus_service)
rpc.listen(8080)