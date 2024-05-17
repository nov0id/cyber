import socket
import threading
import base64
from tkinter import Tk, Text, Entry, Button, END, DISABLED, NORMAL, Label, Toplevel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.text_area = Text(master, state=DISABLED, wrap='word', height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.entry_box = Entry(master, width=40)
        self.entry_box.pack(padx=10, pady=(0, 10))

        self.send_button = Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect(("127.0.0.1", 9999))
            self.display_message("Connected to server.")
        except Exception as e:
            self.display_message(f"Connection error: {e}")
            return

        self.login_window = Toplevel()
        self.login_window.title("Login or Create Account")

        self.username_label = Label(self.login_window, text="Username:")
        self.username_label.pack(padx=10, pady=(10, 0))

        self.username_entry = Entry(self.login_window)
        self.username_entry.pack(padx=10, pady=(0, 10))

        self.private_key_label = Label(self.login_window, text="Private Key (paste from clipboard):")
        self.private_key_label.pack(padx=10, pady=(10, 0))

        self.private_key_entry = Entry(self.login_window)
        self.private_key_entry.pack(padx=10, pady=(0, 10))

        self.login_button = Button(self.login_window, text="Login", command=self.login_request)
        self.login_button.pack(padx=10, pady=(0, 10))

        self.create_account_button = Button(self.login_window, text="Create Account", command=self.create_account)
        self.create_account_button.pack(padx=10, pady=(0, 10))

        self.receive_thread = threading.Thread(target=self.handle_receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.username = None
        self.private_key = None

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
                    self.display_message("Login successful.")
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
        if message:
            try:
                self.server_socket.send(f"{self.username}:{message}".encode())
                self.display_message(f"You: {message}")
                self.entry_box.delete(0, END)
            except Exception as e:
                self.display_message(f"Failed to send message: {e}")

    def display_message(self, message):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED)
        self.text_area.see(END)

def main():
    root = Tk()
    client = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
