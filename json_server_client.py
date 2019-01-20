import socket
import json

class JsonEmitter(object):
    """
    You give it binary chunks of JSON, it emits whole JSON objects.
    """
    def __init__(self, on_new_msg=None):
        self.chunks_string = []
        self.messages = []
        self.delimiter = '\n'
        self.on_new_msg = on_new_msg

    def push_binary_chunk(self, chunk):
        decoded_string = chunk.decode('utf-8')
        if self.delimiter in decoded_string:
            decoded_string_split = decoded_string.split(self.delimiter)

            # emit first message
            first_msg = "".join(self.chunks_string) + decoded_string_split[0]
            self.messages.append(json.loads(first_msg))
            if self.on_new_msg:
                self.on_new_msg(self.messages.pop())
            self.chunks_string = []

            # emit any messages between first msg and the last chunk
            inbetween_msgs = decoded_string_split[1:-1]
            for msg in inbetween_msgs:
                self.messages.append(json.loads(msg))
                if self.on_new_msg:
                    self.on_new_msg(self.messages.pop())

            # save next unfinished msg
            self.chunks_string = decoded_string_split[-1]
        else:
            self.chunks_string.append(decoded_string)

    def pop(self):
        return self.messages.pop(0)

class JsonServer(object):
    '''
    Listens on the specified address and emits messages.

    Example:
    >>> msg_emitter = Utf8MesssageEmitter(lambda msg: print(json.loads(msg)), delimiter)
    >>> json_emitter = TcpMessageEmitter(('localhost', 10000), msg_emitter)
    >>> json_emitter.start()
    '''
    def __init__(self, on_request):
        self.chunks_string = []
        self.json_emitter = JsonEmitter(self.write_response)
        self.on_request = on_request
        self.req_counter = 0

    def listen(self, port):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        print('Listening on localhost:%s' % port)
        sock.bind(('localhost', port))

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            # print('Waiting for a connection')
            self.connection, client_address = sock.accept()
            try:
                # print('Connection from', client_address)
                while True:
                    data = self.connection.recv(4096)
                    if not data:
                        break
                    self.json_emitter.push_binary_chunk(data)
            finally:
                # Clean up the connection
                self.connection.close()

    def write_response(self, msg):
        res = self.on_request(msg)
        self.connection.sendall((json.dumps(res) + '\n').encode('utf-8'))
        self.req_counter += 1
        if self.req_counter % 1000 == 0:
            print('server req counter', self.req_counter)

class JsonClient(object):
    def __init__(self, port):
        self.client = socket.socket()
        self.client.connect(('localhost', port))

    def _send_request(self, json_obj):
        json_emitter = JsonEmitter()
        json_string = json.dumps(json_obj) + '\n'
        self.client.sendall(json_string.encode('utf-8'))
        while not json_emitter.messages:
            data = self.client.recv(4096)
            if not data:
                break
            json_emitter.push_binary_chunk(data)
        if json_emitter.messages:
            return json_emitter.pop()
        else:
            return None

    def __getattr__(self, method):
        def send_request_bound(params):
            return self._send_request({ "method": method, "params": params })
        return send_request_bound