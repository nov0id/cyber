import socket
import threading
import base64
import customtkinter as ctk
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class ChatClient:
    def __init__(self, master):
        self.master = master
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.master.title("Nyx Chat v1.0 Client")

        self.text_area = ctk.CTkTextbox(master, state=ctk.DISABLED, wrap='word', height=400, width=500)
        self.text_area.pack(padx=10, pady=10)

        self.entry_box = ctk.CTkEntry(master, width=400)
        self.entry_box.pack(padx=10, pady=(0, 10))

        self.send_button = ctk.CTkButton(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10))
        #Attempts to connect to the server @LOCAL:9999
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect(("127.0.0.1", 9999))
            self.display_message("Connected to server.")
        except Exception as e:
            self.display_message(f"Connection error: {e}")
            return

        self.login_window = ctk.CTkToplevel()
        self.login_window.title("Login or Request Account")

        self.username_label = ctk.CTkLabel(self.login_window, text="Username:")
        self.username_label.pack(padx=10, pady=(10, 0))

        self.username_entry = ctk.CTkEntry(self.login_window)
        self.username_entry.pack(padx=10, pady=(0, 10))

        self.private_key_label = ctk.CTkLabel(self.login_window, text="Private Key (paste from clipboard):")
        self.private_key_label.pack(padx=10, pady=(10, 0))

        self.private_key_entry = ctk.CTkEntry(self.login_window)
        self.private_key_entry.pack(padx=10, pady=(0, 10))

        self.login_button = ctk.CTkButton(self.login_window, text="Login", command=self.login_request)
        self.login_button.pack(padx=10, pady=(0, 10))

        self.create_account_button = ctk.CTkButton(self.login_window, text="Create Account", command=self.create_account)
        self.create_account_button.pack(padx=10, pady=(0, 10))

        self.receive_thread = threading.Thread(target=self.handle_receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.username = None
        self.private_key = None
        self.server_public_key = None

    def login_request(self):
        self.username = self.username_entry.get()
        private_key_pem = self.private_key_entry.get().encode()

        try:
            self.private_key = serialization.load_pem_private_key(private_key_pem, password=None)
            login_message = f"LOGIN_REQUEST:{self.username}"
            self.server_socket.send(login_message.encode())
        except Exception as e:
            self.display_message(f"Login request failed: {e}")

    def create_account(self):
        username = self.username_entry.get()
        if username:
            try:
                self.server_socket.send(f"REQUEST_USER_CREATION:{username}".encode())
                self.display_message(f"Account creation request sent for {username}. Please wait for approval.")
            except Exception as e:
                self.display_message(f"Error sending account creation request: {e}")

    def handle_receive(self):
        try:
            while True:
                message = self.server_socket.recv(1024).decode()
                if message.startswith("CHALLENGE:"):
                    challenge = message.split(":")[1]
                    self.handle_challenge(challenge)
                elif message == "LOGIN_SUCCESS":
                    self.login_window.destroy()
                    self.master.title(f"Chat Client: {self.username}")
                    self.display_message("Login successful.")
                    self.server_socket.send(f"PKEY_REQUEST:{self.username}".encode())
                    public_key_pem = self.private_key.public_key().public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                elif message.startswith("PKEY:"):
                    server_public_key_pem = base64.urlsafe_b64decode(message.split(":")[1].encode())
                    self.server_public_key = serialization.load_pem_public_key(server_public_key_pem)
                    self.display_message("Received server public key.")
                elif message.startswith("MSG:"):
                    decrypted_message = self.private_key.decrypt(
                        base64.urlsafe_b64decode(message.split("MSG:")[1].encode()),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    ).decode()
                    self.display_message(decrypted_message)
                elif message == "INVALID_USER":
                    self.display_message("Invalid username or user not approved.")
                elif message == "INVALID_RESPONSE":
                    self.display_message("Invalid response to challenge.")
                else:
                    if message:
                        self.display_message(message)
                    else:
                        self.display_message("Server disconnected.")
                        break
        except Exception as e:
            self.display_message(f"Connection error: {e}")

    def handle_challenge(self, challenge):
        try:
            challenge_response = self.private_key.sign(
                challenge.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            challenge_response_b64 = base64.urlsafe_b64encode(challenge_response).decode()
            response_message = f"CHALLENGE_RESPONSE:{self.username}:{challenge_response_b64}"
            self.server_socket.send(response_message.encode())
        except Exception as e:
            self.display_message(f"Error handling challenge: {e}")

    def send_message(self):
        message = self.entry_box.get()
        if message and self.server_public_key:
            try:
                encrypted_message = self.server_public_key.encrypt(
                    f"{self.username}: {message}".encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                signature = self.private_key.sign(
                    encrypted_message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                hashes.SHA256()
                )
                self.server_socket.send(f"MSG:{base64.urlsafe_b64encode(encrypted_message).decode()}:{base64.urlsafe_b64encode(signature).decode()}".encode())
                self.display_message(f"You: {message}")
                self.entry_box.delete(0, ctk.END)
            except Exception as e:
                self.display_message(f"Failed to send message: {e}")

    def display_message(self, message):
        self.text_area.configure(state=ctk.NORMAL)
        self.text_area.insert(ctk.END, message + '\n')
        self.text_area.configure(state=ctk.DISABLED)
        self.text_area.see(ctk.END)

def main():
    root = ctk.CTk()
    ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()