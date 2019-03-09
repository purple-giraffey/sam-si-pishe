import socket
import sys
import json

from json_server_client import JsonClient

json_client = JsonClient(8080)

def get_successors(words_tuple):
    return json_client.get_successors({ "words": list(words_tuple) })

def get_predecessors(words_tuple):
    return json_client.get_predecessors({ "words": list(words_tuple) })

def get_random_word(from_which):
    return json_client.send_request({ "method": "get_random_word_tuple", "params": { "from_which": from_which }})