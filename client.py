import struct
import socket
import time
import sys

if __name__ == "__main__":

    recv_buffer = 1024

    # read command line input
    if len(sys.argv) != 3:
        print("Please define destination host IP as the first argument and port as the second one")
        sys.exit()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    s = socket.socket()

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('Destination host is unreachable')
        sys.exit()

    seq_num = 0
    print("Pinging " + host)
    while seq_num < 4:
        seq_num += 1
        pdata = struct.pack("!Hd", seq_num, time.time())
        s.send(pdata)
        data = s.recv(recv_buffer)
        (seq, timestamp) = struct.unpack("!Hd", data)
        delay = time.time() - timestamp
        delay *= 1000
        print("Reply from " + host + ": time=" + str(delay) + "ms")
        time.sleep(1)
    print("\nSent packets:" + str(seq_num))