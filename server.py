import sys
import socket
import _thread
import time
import signal
from Libs import Connection


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((socket.gethostname(), 5005))
server_socket.listen(5)

opened_cameras = {}


def signal_handler(signal=None, frame=None):
    exit(0)
    


# Loop and check for new connections
while 1:
    try:
        client_socket, address = server_socket.accept()
        print
        "Conencted to - ", address, "\n"
        cam_url = client_socket.recv(4096)
        if cam_url not in opened_cameras:
            client = Connection.Connection([client_socket, cam_url])
            opened_cameras[cam_url] = client
            _thread.start_new_thread(client.capture, (opened_cameras,))

        else:
            opened_cameras[cam_url].addConnection(client_socket)

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        server_socket.close()

        del connections
        exit(0)


