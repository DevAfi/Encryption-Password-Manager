import getpass
from datetime import datetime
from crypto import hash_password, verify_master_password, encrypt_pass, decrypt_pass, generate_password
from storage import save_master_password_hash, load_master_password_hash, load_entries, save_entries
import pyperclip

def setup_master_password():
    print("\n==== FIRST TIME SETUP ====")
    print("Create a master password, this will be needed to access passowrds")
    
    while True: 
        """BTW ------   switch from getpass.getpass to input to be able to see input"""
        input_password = getpass.getpass("Enter master password:  ")
        confirm_password = getpass.getpass("Confirm master password:  ")

        if input_password == confirm_password:
            if len(input_password) < 8:
                print("Password must be at least 8 characters")
                continue
            hashed_input = hash_password(input_password)
            save_master_password_hash(hashed_input)
            print("!!! Master password created successfully !!!")
            return True
        else:
            print("Passwords don't match, please try again")


def login():
    stored_hash = load_master_password_hash()
    att = 4

    while att > 0:
        print("\n==== LOGIN ====")
        password = getpass.getpass("Enter master password:  ")

        if verify_master_password(password, stored_hash):
            print("!!! Access Granted !!!")
            return password
        else:
            att -= 1
            if att > 0:
                print(f"x Incorrect password. {att} attempts remaining")
            else:
                print("\nx Too many failed attempts, Goodbye.")
                exit()
    return None

def generate_password_menu():
    """generate a password, menu to do that"""
    print("\n==== GENERATE PASSWORD ====")

    try:
        length = int(input("Please enter a length (default = 16):       ") or 16)
        use_symbols = input("Would you like to use symbols? (y/n, default = y):        ").lower() != "n"

        password = generate_password(length, use_symbols)

        print(f"\nGenerated password: {password}")
        pyperclip.copy(password)
        print("✓ Copied to clipboard!")
        
    except ValueError:
        print("✗ Invalid length!")



def search_for_service(master_pass):
    entries = load_entries()

    print("\n==== SEARCH FOR PASSWORD ====")


    search_term = input("Enter a service name (E.G., git, youtube, gmail):  ").strip().lower()
    matches = []

    for entry in entries:
        if search_term in entry['service'].strip().lower():
            matches.append(entry)
    
    for i, entry in enumerate(matches, 1):
        print(f"{i}. MATHCES {entry['service']} ({entry['username']})")
    
    choice = int(input("\nEnter your choice here:   "))

    if choice < 1 or choice > len(matches):
        print("x Invalid choice")
        return

    selected = matches[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    print("\n==== INFORMATION ====")
    print("ID:  ", selected['id'])
    print("Service: ", selected['service'])
    print("Username:    ", selected['username'])
    print("Password:    ", decrypted_pass)
    






def add_password(master_pass: str):
    print("\n==== Add a new password ====")
    site = input("Service name (e.g., YouTube, Gmail, GitHub):  ").strip()
    username = input("Enter username/email: ").strip()

    gen_pass = input("Generate password? Y/N:       ")


    if gen_pass.lower() == "y":
        generate_password_menu()

    password = getpass.getpass("Password:   ")

    if not site or not username or not password:
        print("x All fields must be completed")
        return
    
    encrypted_password = encrypt_pass(password, master_pass)

    entries = load_entries()
    next_id_num = len(entries)+1

    new_entry = {
        'id': next_id_num,
        'service': site,
        'username': username,
        'password': encrypted_password,
        'created': datetime.now().strftime('%y-%m-%d')
    }

    entries.append(new_entry)
    save_entries(entries)
    print("\n!!! SUCCESS !!!")
    print("Password added for {site} successfully")

def get_password(master_pass: str) -> str:
    entries = load_entries()

    if len(entries) < 1:
        print("No entries available")
        return
    print("\nStored Services:")

    view_type = int(input("Search(1) or list all services(2)?   "))

    if view_type == 1:
        search_for_service(master_pass)
        return

    #Iterates through all entries and displays them
    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['service']} ({entry['username']})")

    #Asks users choice and validates it
    choice = int(input("\nEnter your choice here:   "))

    if choice < 1 or choice > len(entries):
        print("x Invalid choice")
        return

    selected = entries[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    print("\n==== INFORMATION ====")
    print("ID:  ", selected['id'])
    print("Service: ", selected['service'])
    print("Username:    ", selected['username'])
    print("Password:    ", decrypted_pass)

def delete_password() -> str:
    entries = load_entries()

    if len(entries) < 1:
        print("No entries available")
        return
    print("\nStored Services:")

    #Iterates through all entries and displays them
    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['service']} ({entry['username']})")

    #Asks users choice and validates it
    choice = int(input("\nEnter your choice here:   "))

    if choice < 1 or choice > len(entries):
        print("x Invalid choice")
        return


    confirm = input("\nCONFIRM DELETE (y/n):      ").lower()

    if confirm == "y":
        del entries[choice-1]
        save_entries(entries)

def update_password(master_pass: str):
    """Updates password"""
    entries = load_entries()

    if len(entries) < 1:
        print("No entries available")
        return
    print("\nStored Services:")

    #Iterates through all entries and displays them
    for i, entry in enumerate(entries, 1):
        print(f"{i}. {entry['service']} ({entry['username']})")

    #Asks users choice and validates it
    choice = int(input("\nEnter your choice here:   "))

    if choice < 1 or choice > len(entries):
        print("x Invalid choice")
        return

    selected = entries[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    print("\n==== INFORMATION ====")
    print("ID:  ", selected['id'])
    print("Service: ", selected['service'])
    print("Username:    ", selected['username'])
    print("Password:    ", decrypted_pass)

    try:
        update_choice = int(input("Would you like to change your password(1), username(2) or both(3)?  "))
    except ValueError:
        print("INVALID")
        return
    
    new_username = selected['username']
    new_password = selected['password']  # Keep encrypted

    if update_choice == 1:
        # Update password only
        password = getpass.getpass("Enter new password: ")
        if not password:
            print("✗ Password cannot be empty")
            return
        new_password = encrypt_pass(password, master_pass)
        
    elif update_choice == 2:
        # Update username only
        username = input("Enter new username: ").strip()
        if not username:
            print("✗ Username cannot be empty")
            return
        new_username = username
        
    elif update_choice == 3:
        # Update both
        username = input("Enter new username: ").strip()
        password = getpass.getpass("Enter new password: ")
        if not username or not password:
            print("✗ Fields cannot be empty")
            return
        new_username = username
        new_password = encrypt_pass(password, master_pass)
        
    else:
        print("✗ Invalid choice")
        return

    # Update the entry
    entries[choice - 1] = {
        'id': selected['id'],
        'service': selected['service'],
        'username': new_username,
        'password': new_password,
        'created': selected['created']
    }

    save_entries(entries)
    print(f"✓ Password for '{selected['service']}' updated successfully!")

def main_menu(master_pass: str):
    running = True
    while running:
        print("\n" + "="*40)
        print("PASSWORD MANAGER MENU")
        print("="*40)
        print("1 - Add a new password")
        print("2 - Retrieve a password")
        print("3 - Update a password")
        print("4 - Delete a password")
        print("5- Exit")

        choice = int(input("\nEnter choice: "))

        if choice < 1 or choice > 5:
            print("Invalid choice")
        

        if choice == 1:
                add_password(master_pass)
        elif choice == 2:
            get_password(master_pass)
        elif choice == 3:
            update_password(master_pass)
        elif choice == 4:
            delete_password()
        else:
            print("GOODBYE!")
            running = False

        """match choice:
            case 1:
                add_password(master_pass)
            case 2:
                get_password(master_pass)
            case 3:
                exit()"""

def main():
    print("Password Manager")
    running = True

    stored_hash = load_master_password_hash()

    if not stored_hash:
        setup_master_password()
        master_pass = login()
    else:
        master_pass = login()

    print ("\nWelcome to the manager")

    main_menu(master_pass)

if __name__ == "__main__":
    main()