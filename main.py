import getpass
from datetime import datetime
from crypto import hash_password, verify_master_password, encrypt_pass
from storage import save_master_password_hash, load_master_password_hash, load_entries, save_entries

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

def add_password(master_pass: str):
    print("\n==== Add a new password ====")
    site = input("Service name (e.g., YouTube, Gmail, GitHub):  ").strip()
    username = input("Enter username/email: ").strip()
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


def main():
    print("Password Manager")

    stored_hash = load_master_password_hash()

    if not stored_hash:
        setup_master_password()
        master_pass = login()
    else:
        master_pass = login()


    



    print ("\nWelcome to the manager")
    #add_password(master_pass)

if __name__ == "__main__":
    main()