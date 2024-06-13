#Deletes the user and key files in the case we need to emergency reset the server (dev or emercency)

import os

def main():
    clean_list = ["users.json", "server_private_key.pem", "server_public_key.pem"]
    for file_name in clean_list:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Old {file_name} file deleted.")
        else:
            print(f"No {file_name} file found.")


#Checks to see if this is being imported as a class or being run explicitly
if __name__ == "__main__":
    main()


