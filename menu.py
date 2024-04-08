import sys
from os import system

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
    function_names = [messages, appointment, logout]
    menu_items = dict(enumerate(function_names, start=1))

    while True:
        print("Welcome to Cat Clinic meooooooooooow :3")
        print("""1. View messages
2. Book an appointment
3. Logout""")
        choice = int(input("Please enter your choice (1-3): "))  # Get function key
        try:
            selected_value = menu_items[choice]
        except:
            print("Invalid choice")
            continue
        selected_value()  # add parentheses to call the function

if __name__ == "__main__":
    main()