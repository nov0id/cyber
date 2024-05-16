import os
import socket
import sys
import hashlib
import logging
from termcolor import colored
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256

# Configure logging
logging.basicConfig(level=logging.INFO)

# Receiving The Value Of IP and PORT From the User
LISN_IP = input(colored("Enter The Local IP of your Machine: ", "green"))
LISN_PORT = int(input(colored("Enter The port no. to bind: ", "green")))
USER_NAME = input(colored("Please Choose a Username for Chat: ", "green"))

os.system('clear')
print(colored("<1>ONLINE...", "green", attrs=['reverse', 'blink']))

name = USER_NAME + ">> "
encoded_name = name.encode()

def derive_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return ct

def decrypt_message(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    message = decryptor.update(ciphertext) + decryptor.finalize()
    return message

def chat():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LISN_IP, LISN_PORT))
    s.listen(1)
    conn, addr = s.accept()
    print(colored(f"[+] {addr} Connected", "green"))

    # Placeholder for secure key exchange to get key and iv
    password = b'secure_shared_secret'  # Replace with a proper key exchange mechanism
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)

    while True:
        msg = input(colored("\nSEND-> ", "red", attrs=['bold']))
        if msg == 'bye':
            conn.send('bye'.encode())
            os.system('clear')
            print(colored("<0>OFFLINE", "red", attrs=['bold']))
            conn.close()
            sys.exit()
            break
        else:
            data = encoded_name + msg.encode()
            data_send = encrypt_message(data, key, iv)
            conn.send(data_send)
            hash_object = hashlib.sha256(msg.encode())
            hash_value = hash_object.hexdigest()
            print(f"Hash value of message: {hash_value}")

            In_msg = conn.recv(8192)
            recv_data_enc = decrypt_message(In_msg, key, iv)
            recv_data_unenc = recv_data_enc.decode()
            print("\n" + recv_data_unenc)

def main():
    chat()

if __name__ == "__main__":
    main()