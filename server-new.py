import socket
import json

class Utf8MesssageEmitter(object):
    '''
    You dump binary chunks into this, and it emits decoded messages
    which are split by the delimiter.

    For example:
    >>> emitter = Utf8MesssageEmitter(lambda msg: print('got msg:', msg))
    >>> emiiter.push_binary_chunk(b'hello ')
    >>> emmiter.push_binary_chunk(b'world\nhi')
    >>> emmiter.push_binary_chunk(b' there\n')

    will print:
    > got msg: hello world
    > got msg: hi there
    '''
    def __init__(self, on_new_msg, delimiter='\n'):
        self.chunks_string = []
        self.delimiter = delimiter
        self.on_new_msg = on_new_msg

    def push_binary_chunk(self, chunk):
        decoded_string = chunk.decode('utf-8')
        if self.delimiter in decoded_string:
            decoded_string_split = decoded_string.split(self.delimiter)

            # emit first message
            first_msg = "".join(self.chunks_string) + decoded_string_split[0]
            self.on_new_msg(first_msg)
            self.chunks_string = []

            # emit any messages between first msg and the last chunk
            inbetween_msgs = decoded_string_split[1:-1]
            for msg in inbetween_msgs:
                self.on_new_msg(msg)

            # save next unfinished msg
            self.chunks_string = decoded_string_split[-1]
        else:
            self.chunks_string.append(decoded_string)

class TcpMessageEmitter(object):
    '''
    Listens on the specified address and emits messages.

    Example:
    >>> msg_emitter = Utf8MesssageEmitter(lambda msg: print(json.loads(msg)), delimiter)
    >>> json_emitter = TcpMessageEmitter(('localhost', 10000), msg_emitter)
    >>> json_emitter.start()
    '''
    def __init__(self, server_address, msg_emitter):
        self.server_address = server_address
        self.msg_emitter = msg_emitter

    def start(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        print('Starting up on %s port %s' % self.server_address)
        sock.bind(self.server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            print('Waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('Connection from', client_address)
                while True:
                    data = connection.recv(4096)
                    self.msg_emitter.push_binary_chunk(data)
            finally:
                # Clean up the connection
                connection.close()

msg_emitter = Utf8MesssageEmitter(lambda msg: print(json.loads(msg)), delimiter='\n')
json_emitter = TcpMessageEmitter(('localhost', 10001), msg_emitter)
json_emitter.start()