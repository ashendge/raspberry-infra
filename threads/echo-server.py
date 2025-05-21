"""
Multithreaded Echo Server in Python
This is a simple echo server that uses the socket and threading modules to handle multiple clients concurrently.

It listens for incoming connections on a specified port 7050 and echoes back any data received from the client.
The server runs indefinitely until interrupted by the user.

The fun part is that it uses threading to handle multiple clients at the same time, so you can connect to the server with multiple clients.
It creats a new thread for each client and handles the communication in that thread. It involes creating a new file descriptor for each client connection.
The server is implemented using the socket module to create a TCP socket and the threading module to handle multiple clients concurrently.

The server listens for incoming connections on a specified port and creates a new thread for each client that connects. 
The listening socket is set to non-blocking mode, so it can handle multiple clients at the same time. 
The server uses a while loop to continuously accept new connections and create new threads for each client.

The server runs indefinitely until interrupted by the user. The server can be stopped by pressing Ctrl+C in the terminal where it is running.
"""

import socket
import threading
import time
import os

def print_accept_queue_size():
    """
    Print the size of the accept queue in the kernel every 5 seconds.
    """
    while True:
        try:
            # Read the /proc/net/tcp file to get the accept queue size
            with open('/proc/net/tcp', 'r') as f:
                lines = f.readlines()
                # Filter for the server's port (7050 in hex is 1B8A)
                queue_info = [
                    line.split()[4] for line in lines[1:]
                    if '1B8A' in line.split()[1]
                ]
                if queue_info:
                    recv_queue, send_queue = queue_info[0].split(':')
                    print(f"Accept Queue Size: {int(recv_queue, 16)}")
                else:
                    print("No connections in the accept queue.")
        except Exception as e:
            print(f"Error reading accept queue size: {e}")
        time.sleep(5)


def handle_client_request(client_socket, addr):
    """
    Handle the client request
    This function receives data from the client and sends it back to the client.
    It runs in a separate thread for each client.
    """
    # while loop needed to keep the connection open and handle multiple messages
    # from the client
    print(f"Handling {addr} in process")
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            # Echo the data back to the client
            client_socket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7050))
    server.listen(5)
    print("Listening on port 7050...")

    # Start a thread to monitor the accept queue size
    threading.Thread(target=print_accept_queue_size, args=(), daemon=True).start()
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client_request, args=(client_socket, addr))
        thread.start()

if __name__ == '__main__':
    main()
