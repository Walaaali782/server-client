import socket
import threading

def connect_to_server():
    client_name = input("Enter your name: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8081))
    client_socket.send(client_name.encode('utf-8'))
    print("Connected to server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            client_socket.send(message.encode('utf-8'))
            break
        elif ':' in message:
            client_socket.send(message.encode('utf-8'))
            print("Message sent successfully.")
        else:
            print("Invalid message format. Use 'recipient_name: message' for private message or 'exit' to disconnect.")

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

if __name__ == "__main__":
    connect_to_server()

