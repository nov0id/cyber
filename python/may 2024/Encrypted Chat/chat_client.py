import os
import socket
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
SERVER_IP = input(colored("What Is Ip of the server running: ", "green"))
SERVER_PORT = int(input(colored("Enter Port No on which the server is running: ", "green")))
USER_NAME = input(colored("Please Choose a Username for Chat: ", "green"))

os.system('clear')
print(colored("<1>ONLINE..", "green", attrs=['reverse', 'blink']))

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
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))

        # Placeholder for secure key exchange to get key and iv
        password = b'secure_shared_secret'  # Replace with a proper key exchange mechanism
        salt = os.urandom(16)
        key = derive_key(password, salt)
        iv = os.urandom(16)

        while True:
            In_msg = s.recv(8192)
            try:
                recv_data_1 = decrypt_message(In_msg, key, iv)
                recv_data_unenc = recv_data_1.decode('utf-8')
            except (UnicodeDecodeError, ValueError) as e:
                logging.error(f"Decryption/Decoding error: {e}")
                recv_data_unenc = recv_data_1  # Fallback to raw data

            hash_object = hashlib.sha256(recv_data_unenc.encode())
            hash_value = hash_object.hexdigest()
            logging.info(f"Hash value of message: {hash_value}")

            if recv_data_unenc.strip() == 'bye':
                s.send('bye'.encode())
                os.system('clear')
                print(colored("<0>OFFLINE", "red", attrs=['bold']))
                s.close()
                break

            print("\n" + recv_data_unenc)

            Out_msg = input(colored("\nSEND-> ", "red", attrs=['bold']))
            if Out_msg == 'bye':
                s.send(Out_msg.encode())
                os.system('clear')
                print(colored("<0>OFFLINE", "red", attrs=['bold']))
                s.close()
                break
            else:
                data = encoded_name + Out_msg.encode()
                send_data = encrypt_message(data, key, iv)
                s.send(send_data)

    except Exception as e:
        logging.error(f"Connection error: {e}")
    finally:
        s.close()

def main():
    chat()

if __name__ == "__main__":
    main()
