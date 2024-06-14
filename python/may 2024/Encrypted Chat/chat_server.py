#Imports neccesary libraries
import socket
import threading
import json
import os
import base64
import getpass
import customtkinter as ctk
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Global dictionaries initialization
# Holds all registered users
users = {}
# Stores active user requests
user_requests = {}
# Stores actively connected users
clients = {}
# Stores challenges for user authentication
challenges = {}
# Stores the public keys of actively connected clients
client_public_keys = {}

# GUI class for the server
class ServerGUI:
    def __init__(self, master):
        #Sets reference to 'master' or our instance of our GUI
        self.master = master

        #Sets the theme of the GUI
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        #Sets title
        self.master.title("Nyx Chat v1.0 Server")

        self.text_area = ctk.CTkTextbox(master, state=ctk.DISABLED, wrap='word', height=400, width=500)
        self.text_area.pack(padx=10, pady=10)

        self.entry_box = ctk.CTkEntry(master, width=400)
        self.entry_box.pack(padx=10, pady=(0, 10))

        self.send_button = ctk.CTkButton(master, text="Send", command=self.process_command)
        self.send_button.pack(padx=10, pady=(0, 10))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", 9999))
        self.server_socket.listen(5)
        self.log("Server listening on port 9999")

        self.server_private_key, self.server_public_key = load_or_generate_server_keys()

        #Begins actively listening for clients
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()

    def log(self, message):
        self.text_area.configure(state=ctk.NORMAL)
        self.text_area.insert(ctk.END, message + '\n')
        self.text_area.configure(state=ctk.DISABLED)
        self.text_area.see(ctk.END)

    def accept_clients(self):
        while True:
            #Listens for new connections and accepts them
            client_socket, addr = self.server_socket.accept()
            self.log(f"Accepted connection from {addr}")
            #Starts a thread for handling the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, self.log, self.server_private_key, self.server_public_key))
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
        self.entry_box.delete(0, ctk.END)

# Load or generate server keys, this function returns the variables private_key, public_key
def load_or_generate_server_keys():
    #Checks to see if keys are already created
    if os.path.exists('server_private_key.pem') and os.path.exists('server_public_key.pem'):
        # Prompt for password to load existing keys
        password = getpass.getpass("Enter password to load server private key: ").encode()
        #Opens private key file and saves it to private_key_pem
        with open('server_private_key.pem', 'rb') as f:
            private_key_pem = f.read()
        #Opens public key file and saves it to public_key_pem
        with open('server_public_key.pem', 'rb') as f:
            public_key_pem = f.read()
        #Sterilizes our variables into ones our cryptography functions will be able to process
        private_key = serialization.load_pem_private_key(private_key_pem, password=password)
        public_key = serialization.load_pem_public_key(public_key_pem)
    else:
        # Generate new keys and prompt for password to encrypt private key
        password = getpass.getpass("Enter password to encrypt server private key: ").encode()
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        #Writes the private key to a file after it is generated
        with open('server_private_key.pem', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password)
            ))
        #Writes the public key to a file after it is generated
        with open('server_public_key.pem', 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    return private_key, public_key

# Function to save users to a JSON file
def save_users_to_file():
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Function to load users from a JSON file
def load_users_from_file():
    global users
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)

# Function to broadcast a message to all connected clients except the sender. Arguments are the message to be sent
# (in plaintext) with no prefix, and the senders socket to be excluded from the process
def broadcast_message(message, sender_socket):
    #Iterates over the clients dictionary and extracts the username and client_socket
    for username, client_socket in clients.items():
        #If user is not sender continue
        if client_socket != sender_socket:
            try:
                # Retrieves the connected users public key from file and encrypts the message. Adds prefix for client interpretation
                public_key = serialization.load_pem_public_key(users[username]['public_key'].encode())
                encrypted_message = public_key.encrypt(
                    message.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                client_socket.send(f"MSG:{base64.urlsafe_b64encode(encrypted_message).decode()}".encode())
            #Handles any possible exceptions
            except Exception as e:
                print(f"Error sending message: {e}")

# Handler for communication with a client
def handle_client(client_socket, addr, log_func, server_private_key, server_public_key):
    log_func(f"Handling client from {addr}")
    try:
        while True:
            # Waits for a message from the client, and decodes in bytes to the 'message' string for handling
            message = client_socket.recv(1024).decode()
            # If message is blank, this is a signal that the client has disconnected
            if not message:
                log_func("Client disconnected")
                #Breaks to 'Finally' in order to handle removal of the client from the clients dictionary that stores
                #actively connected users
                break
            #Uncomment to show undecrypted raw verbose of all messages received on the server
            log_func(f"Received message from {addr}: {message}")
            #Handles user creation requests
            if message.startswith("REQUEST_USER_CREATION"):
                username = message.split(":")[1]
                #If user account doesn't exist, we append the creation request for further manual approval. If not we deny and inform
                if username not in users:
                    user_requests[username] = (client_socket, addr)
                    log_func(f"User creation request received for {username} from {addr}")
                else:
                    log_func(f"Denied user account creation request automatically. Account already exists.")
                    client_socket.send(f"INVALID_USER".encode())
            # Handles login requests from the client by responding with a challenge to be signed with thier private key.
            #Prevents messages from being handled by users who are not "logged in" as they will likely not have the public
            #key to our server
            elif message.startswith("LOGIN_REQUEST"):
                username = message.split(":")[1]
                if username in users:
                    # Generates challenge, sterilizes with base64 encoding, and is then decoded to UTF-8
                    challenge = base64.urlsafe_b64encode(os.urandom(32)).decode()
                    challenges[username] = challenge
                    # Sends challenge to client
                    client_socket.send(f"CHALLENGE:{challenge}".encode())
                else:
                    client_socket.send(b"INVALID_USER")
            #Listens for a challenge response from clients. Handles all exceptions.
            elif message.startswith("CHALLENGE_RESPONSE"):
                # Slices list excluding the first index 0 which is the Handler identifier
                username, response = message.split(":")[1:]
                # Checks to see if a challenge exists for the user responding, if not, sends a "INVALID_USER" to the client
                if username in challenges:
                    challenge = challenges.pop(username)
                    # Loads the responding user's public key to our variable stored_public_key
                    stored_public_key = serialization.load_pem_public_key(users[username]['public_key'].encode())
                    try:
                        # Verifies the hashed challenge using the public key we got from the previous step, if it fails, the code proceeds to exception
                        stored_public_key.verify(
                            base64.urlsafe_b64decode(response.encode()),
                            challenge.encode(),
                            padding.PKCS1v15(),
                            hashes.SHA256()
                        )
                        # Adds user to the connected clients dictionary, displays login, and sends 'LOGIN_SUCCESS' to the client
                        clients[username] = client_socket
                        log_func(f"User {username} logged in from {addr}")
                        client_socket.send(b"LOGIN_SUCCESS")
                    except Exception as e:
                        client_socket.send(b"INVALID_RESPONSE")
                else:
                    client_socket.send(b"INVALID_USER")
            elif message.startswith("PKEY_REQUEST"):
                client_socket.send(f"PKEY:{base64.urlsafe_b64encode(server_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode()}".encode())
            elif message.startswith("MSG:"):
                #Unpacks our message 
                encrypted_message = base64.urlsafe_b64decode(message.split(":")[1].encode())
                signature = base64.urlsafe_b64decode(message.split(":")[2].encode())
                #Verify signature if not, fail and report activity to the log
                try:
                    #Grabs our public key from the users object using the username established during login
                    public_key = serialization.load_pem_public_key(users[username]['public_key'].encode())
                    public_key.verify(
                        signature,
                        encrypted_message,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                    hashes.SHA256()
                    )
                    #Once the key is verified we can now decrypt our message and broadcast to our peers
                    try:
                        decrypted_message = server_private_key.decrypt(
                            encrypted_message,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        ).decode()
                        log_func(f"Decrypted message from {addr}: {decrypted_message}")
                        #Broadcasts to peers and carries over the 'client_socket' variable to be used for exclusion from broadcast
                        broadcast_message(decrypted_message, client_socket)
                    except Exception as e:
                        log_func(f"Error decrypting message from {addr}: {e}")
                        client_socket.send(b"INVALID_MESSAGE")
                except Exception as e:
                    log_func(f"Signature verification failed from {addr} {e}")
            else:
                client_socket.send(b"INVALID_MESSAGE")
    except Exception as e:
        log_func(f"Error handling client {addr}: {e}")
    finally:
        log_func(f"Closing client socket from {addr}")
        if 'username' in locals() and username in clients:
            del clients[username]
        try:
            client_socket.close()
        except Exception as e:
            log_func(f"Error closing client socket from {addr}: {e}")

# Function to approve a user creation request
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

            log_func(f"User {username} approved from {addr}")
            private_key_str = private_key_pem.decode()
            log_func(f"Private key for user {username}:\n{private_key_str}")
            return None
        except Exception as e:
            log_func(f"Error approving user {username} from {addr}: {e}")
            try:
                client_socket.send(f"Error: {e}".encode())
            except Exception as send_error:
                log_func(f"Error sending error message to client {addr}: {send_error}")
    else:
        log_func(f"No request found for user {username}")
        return None

# Function to deny a user creation request
def deny_request(username, log_func):
    if username in user_requests:
        client_socket, addr = user_requests.pop(username)
        try:
            client_socket.send(b"INVALID_USER")
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


#Main loop
def main():
    load_users_from_file()
    root = ctk.CTk()
    ServerGUI(root)
    root.mainloop()

#Checks to see if this is being imported as a class or being run explicitly
if __name__ == "__main__":
    main()

