import hashlib
import sys
from os import system

def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        with open("credentials.txt", "w") as f:
             f.write(email + "\n")
             f.write(hash1)
        print("Registration successful!")
    else:
        print("Password is not the same! \n")

def login():
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    with open("credentials.txt", "r") as f:
        stored_email, stored_pwd = f.read().split("\n")
    if email == stored_email and auth_hash == stored_pwd:
         print("Logged in Successfully!")
    else:
         print("Failed login! \n")

def messages():
    while True:
        print("Messages:") # Simulate function output.
        #TODO
        key = input("Press Y to go back\n")
        if key == 'y':
            system('cls')  # clears stdout
            break
        else:
            continue

def appointment():
    while True:
        print("Book an appointment")
        # TODO
        key = input("Press Y to go back\n")
        if key == 'y':
            system('cls')  # clears stdout
            break
        else:
            continue

def logout():
    key = input("Press Y to confirm: ")
    if key == 'y':
        system('cls')  # clears stdout
        print("Logging out")
        sys.exit()
    else:
        return

def main():
    function_names = [messages, appointment, logout, signup, login]
    menu_items = dict(enumerate(function_names, start=1))

    while True:
        print("Welcome to Cat Clinic meooooooooooow :3")
        print("""1. View messages
2. Book an appointment
3. Logout
4. Signup
5. Login""")
        choice = int(input("Please enter your choice (1-5): "))  # Get function key
        try:
            selected_value = menu_items[choice]
        except:
            print("Invalid choice")
            continue
        selected_value()  # add parentheses to call the function

if __name__ == "__main__":
    main()
