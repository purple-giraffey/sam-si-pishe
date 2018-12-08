import re
import json
import random
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
print(os.path.join(script_dir, 'mk-books-text.txt'))

def split_in_celini(text):
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

def find_successors(celini, max_n=5, successors = {}):
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
                if key in successors:
                    successors[key].append(val)
                else:
                    successors[key] = [val]


successors = {}
predecessors = {}
counter = 0
with open(os.path.join(script_dir, 'mk-books-text.txt'), 'r', encoding = "utf8") as f:
    for line in f.readlines():
        counter += 1
        if counter % 1000 == 0:
            print (counter)
        celini = split_in_celini(line)
        find_successors(celini, 5, successors)
        find_successors([celina[::-1] for celina in celini], 5, predecessors)
        if counter >= 100000:
            break

def find_word_tuples_len_one(successors):
    word_tuples_len_one = []
    for key in successors:
        if len(key) == 1:
            word_tuples_len_one.append(key)
    return word_tuples_len_one

def find_random_word_tuple(word_tuples_len_one):
    return random.choice(word_tuples_len_one)

successor_word_len_one = find_word_tuples_len_one(successors)
predecessor_word_len_one = find_word_tuples_len_one(predecessors)

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            print('starting loop')
            data = connection.recv(10000000)
            
            if data:
                data = data.decode('utf-8')
                decoded_json_object = json.loads(data)
                print(decoded_json_object)
                if decoded_json_object["action"] == "get_predecessors":
                    words_tuple = tuple(decoded_json_object["words"])
                    response = { "results": predecessors[words_tuple] if words_tuple in predecessors else {} }
                elif decoded_json_object["action"] == "get_successors":
                    words_tuple = tuple(decoded_json_object["words"])
                    response = { "results": successors[words_tuple] if words_tuple in successors else {} }
                elif decoded_json_object["action"] == "get_random_word_tuple":
                    from_which = decoded_json_object["from_which"]
                    response = find_random_word_tuple(successor_word_len_one if from_which == "successors" else predecessor_word_len_one)
                # print('received "%s"' % data)

                print('sending data back to the client')
                print(response)
                json_response = json.dumps(response)
                connection.sendall(json_response.encode('utf-8'))
            else:
                print('no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
