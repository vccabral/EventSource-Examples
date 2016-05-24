from sseclient import SSEClient
import socket
import json


URL = 'https://eventsource.firebaseio-demo.com/.json'

class ClosableSSEClient(SSEClient):
    """
    Hack in some closing functionality on top of the SSEClient
    """

    def __init__(self, *args, **kwargs):
        self.should_connect = True
        super(ClosableSSEClient, self).__init__(*args, **kwargs)

    def _connect(self):
        if self.should_connect:
            super(ClosableSSEClient, self)._connect()
        else:
            raise StopIteration()

    def close(self):
        self.should_connect = False
        self.retry = 0
        # HACK: dig through the sseclient library to the requests library down to the underlying socket.
        # then close that to raise an exception to get out of streaming. I should probably file an issue w/ the
        # requests library to make this easier
        self.resp.raw._fp.fp._sock.shutdown(socket.SHUT_RDWR)
        self.resp.raw._fp.fp._sock.close()


try:
    sse = ClosableSSEClient(URL)
    for msg in sse:
        msg_data = json.loads(msg.data)
        if msg_data is None:    # keep-alives
            continue
        path = msg_data['path']
        data = msg_data['data']
        if path == '/':
            # initial update
            if data:
                keys = data.keys()
                keys.sort()
                for k in keys:
                    print(data[k])
        else:
            # must be a push ID
            print(data)
except socket.error:
    pass    # this can happen when we close the stream

