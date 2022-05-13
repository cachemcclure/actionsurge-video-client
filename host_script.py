### Multi-Video Streaming Program - Host
## Cache McClure
## ActionSURGE

## Import Modules
import socket
import cv2
import pickle
import struct
import imutils
from joblib import Parallel, delayed, parallel_backend

## Get Single Frame from Cam
def get_frame(client_socket,cam_name):
    while True:
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        try:
            cv2.imshow(cam_name,frame)
        except:
            xyz = 0
        key = cv2.waitKey(10)
        if key == 13:
            break
    client_socket.close()

## Get Number of Cams
cam_no = int(input('Number of camera feeds: '))

sockets = {}
for xx in range(cam_no):
    sockets['cam_'+str(xx+1)] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = input('Camera {} Remote IP (shown on their screen): '.format(xx+1))
    port = 10060 + xx
    sockets['cam_'+str(xx+1)].connect((host_ip,port))

##data = b""
##payload_size = struct.calcsize("Q")

Parallel(n_jobs=cam_no,prefer="threads")(delayed(get_frame)(sockets[xx],xx) for xx in sockets)

## Client Socket 1
# Init client socket for cam 1
##client_socket_1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Enter IP for cam 1
##host_ip_1 = input('Remote IP: ')
# Port assignement for cam 1
##port_1 = 10050
# Connect to cam 1
##client_socket_1.connect((host_ip,port))
#Init data var
##data = b""
# Unsigned long int
##payload_size = struct.calcsize("Q")

# Loop to grab a stream of images
##while True:
##    while len(data) < payload_size:
##        packet = client_socket_1.recv(4*1024)
##        if not packet: break
##        data += packet
##    packed_msg_size = data[:payload_size]
##    data = data[payload_size:]
##    msg_size = struct.unpack("Q",packed_msg_size)[0]
##    while len(data) < msg_size:
##        data += client_socket_1.recv(4*1024)
##    frame_data = data[:msg_size]
##    data = data[msg_size:]
##    frame = pickle.loads(frame_data)
##    cv2.imshow("Cam 1",frame)
##    key = cv2.waitKey(10)
##    if key == 13:
##        break
##client_socket_1.close()
