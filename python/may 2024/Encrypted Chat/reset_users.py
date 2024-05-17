#Deletes the user.json file in the case we need to emergency reset the server due to key loss

import os

if os.path.exists("users.json"):
    os.remove("users.json")
    print("Old users.json file deleted.")
else:
    print("No users.json file found.")
