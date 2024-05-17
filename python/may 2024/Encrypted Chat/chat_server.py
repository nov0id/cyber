import socket
import threading
import json
import os
from tkinter import Tk, Text, Entry, Button, END, DISABLED, NORMAL
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

users = {}
user_requests = {}
clients = []

def save_users_to_file():
    with open('users.json', 'w') as f:
        json.dump(users, f)

def load_users_from_file():
    global users
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)

def broadcast_message(message, sender_socket):
    for client_socket, addr in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error sending message to {addr}: {e}")

def handle_client(client_socket, addr, log_func):
    log_func(f"Handling client from {addr}")
    clients.append((client_socket, addr))
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                log_func("Client disconnected")
                break
            log_func(f"Received message from {addr}: {message}")
            if message.startswith("REQUEST_USER_CREATION"):
                username = message.split(":")[1]
                user_requests[username] = (client_socket, addr)
                log_func(f"User creation request received for {username} from {addr}")
            elif message.startswith("LOGIN"):
                username, public_key_pem = message.split(":")[1:]
                if username in users:
                    stored_public_key = serialization.load_pem_public_key(users[username]['public_key'].encode())
                    incoming_public_key = serialization.load_pem_public_key(public_key_pem.encode())
                    if stored_public_key.public_bytes(
                        encoding=serialization.Encoding.PEM, 
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ) == incoming_public_key.public_bytes(
                        encoding=serialization.Encoding.PEM, 
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ):
                        log_func(f"User {username} logged in from {addr}")
                    else:
                        client_socket.send(b"INVALID_USER")
                else:
                    client_socket.send(b"INVALID_USER")
            else:
                username, message = message.split(":", 1)
                broadcast_message(f"{username}> {message}", client_socket)
    except Exception as e:
        log_func(f"Error handling client {addr}: {e}")
    finally:
        log_func(f"Closing client socket from {addr}")
        clients.remove((client_socket, addr))
        try:
            client_socket.close()
        except Exception as e:
            log_func(f"Error closing client socket from {addr}: {e}")

def approve_request(username, log_func):
    if username in user_requests:
        client_socket, addr = user_requests.pop(username)
        try:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            public_key = private_key.public_key()

            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            users[username] = {"public_key": public_key_pem.decode()}
            save_users_to_file()

            client_socket.send(public_key_pem)
            log_func(f"User {username} approved from {addr}")
            private_key_str = private_key_pem.decode()
            log_func(f"Private key for user {username}:\n{private_key_str}")
            return private_key_str
        except Exception as e:
            log_func(f"Error approving user {username} from {addr}: {e}")
            try:
                client_socket.send(f"Error: {e}".encode())
            except Exception as send_error:
                log_func(f"Error sending error message to client {addr}: {send_error}")
    else:
        log_func(f"No request found for user {username}")
        return None

def deny_request(username, log_func):
    if username in user_requests:
        client_socket, addr = user_requests.pop(username)
        try:
            client_socket.send(b"REQUEST_DENIED")
            log_func(f"User {username} denied from {addr}")
        except Exception as e:
            log_func(f"Error denying user {username} from {addr}: {e}")
        finally:
            log_func(f"Closing client socket from {addr}")
            try:
                client_socket.close()
            except Exception as close_error:
                log_func(f"Error closing client socket during denial from {addr}: {close_error}")
    else:
        log_func(f"No request found for user {username}")

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Server GUI")

        self.text_area = Text(master, state=DISABLED, wrap='word', height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.entry_box = Entry(master, width=50)
        self.entry_box.pack(padx=10, pady=(0, 10))

        self.send_button = Button(master, text="Send", command=self.process_command)
        self.send_button.pack(padx=10, pady=(0, 10))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 9999))
        self.server_socket.listen(5)
        self.log("Server listening on port 9999")

        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()

    def log(self, message):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED)
        self.text_area.see(END)

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.log(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, self.log))
            client_handler.start()

    def process_command(self):
        command = self.entry_box.get().strip().split()
        if len(command) == 2:
            action, username = command
            if action == "approve":
                approve_request(username, self.log)
            elif action == "deny":
                deny_request(username, self.log)
            else:
                self.log("Invalid command. Use 'approve <username>' or 'deny <username>'")
        else:
            self.log("Invalid command format. Use 'approve <username>' or 'deny <username>'")
        self.entry_box.delete(0, END)

def main():
    load_users_from_file()
    root = Tk()
    gui = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
