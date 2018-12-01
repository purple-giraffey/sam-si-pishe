import socket
import sys
import json

def ask_server(query):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    sock.connect(server_address)
    try:
        message = json.dumps(query)
        sock.send(message.encode('utf-8'))
        data = sock.recv(10000000)
        return json.loads(data.decode('utf-8'))
    finally:
        sock.close()

def get_successors(words_tuple):
    return ask_server({ "action": "get_successors", "words": list(words_tuple) })["results"]

def get_predecessors(words_tuple):
    return ask_server({ "action": "get_predecessors", "words": list(words_tuple) })["results"]

def get_random_word(from_which):
    return ask_server({ "action": "get_random_word_tuple", "from_which": from_which })[0]