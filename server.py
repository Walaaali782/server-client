import socket
import threading

clients = {}

def start_server():
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8081))
    server_socket.listen(5)
    print("Server started. Waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=client_handler, args=(client_socket,)).start()

def client_handler(client_socket):
    global clients
    client_name = client_socket.recv(1024).decode('utf-8')
    clients[client_name] = client_socket
    print(f"Client connected: {client_name}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            break

        if message.lower() == "exit":
            del clients[client_name]
            client_socket.close()
            print(f"Client disconnected: {client_name}")
            break

        recipient, message = message.split(':', 1)
        recipient = recipient.strip()
        if recipient in clients:
            clients[recipient].send(f"From {client_name}: {message}".encode('utf-8'))
        else:
            client_socket.send("Recipient not found or offline.".encode('utf-8'))

if __name__ == "__main__":
    start_server()
