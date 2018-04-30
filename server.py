import socket
import select
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please define port as the first argument")
        sys.exit()
    else:
        port = int(sys.argv[1])

    clients_list = []
    receive_buffer = 1024
    host = 'localhost'
    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen()
    clients_list.append(server_socket)
    print("Listening on port " + str(port))

    while True:
        read_sockets, write_sockets, error_sockets = select.select(clients_list, [], [])
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                clients_list.append(client_socket)
                print("\nNew client (%s, %s) connected" % addr)
            else:
                try:
                    data = sock.recv(receive_buffer)
                    if data:
                        print("    New ping packet is received from (%s, %s)" % addr)
                        sock.send(data)
                        #(timestamp) = struct.unpack("!Hd", data)
                    else:
                        raise ConnectionResetError()
                except:
                    sock.close()
                    print("\nConnection with host (%s, %s) is finished" % addr)
                    clients_list.remove(sock)
                    continue
