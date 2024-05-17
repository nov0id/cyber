import socket
import threading
from tkinter import Tk, Text, Entry, Button, END, DISABLED, NORMAL, Scrollbar, VERTICAL
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

KEY = b'1234567890abcdef'
IV = b'abcdef1234567890'

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Encrypted Chat Client")

        self.text_area = Text(master, state=DISABLED, wrap='word', height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.scrollbar = Scrollbar(master, orient=VERTICAL, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.entry_box = Entry(master, width=40)
        self.entry_box.pack(padx=10, pady=(0, 10))

        self.send_button = Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10))

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 9999))

        self.receive_thread = threading.Thread(target=self.handle_receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def encrypt_message(self, message):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()
        return decrypted_message.decode()

    def handle_receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024)
                if message:
                    try:
                        decrypted_message = self.decrypt_message(message)
                        self.display_message(decrypted_message)
                    except Exception as e:
                        self.display_message(f"Failed to decrypt message: {e}")
            except:
                break

    def send_message(self):
        message = self.entry_box.get()
        if message:
            encrypted_message = self.encrypt_message(message)
            self.client_socket.send(encrypted_message)
            self.entry_box.delete(0, END)

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