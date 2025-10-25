import getpass
from datetime import datetime
from crypto import hash_password, verify_master_password, encrypt_pass, decrypt_pass, generate_password
from storage import save_master_password_hash, load_master_password_hash, load_entries, save_entries
from password_analyzer import calculate_strength, display_strength_analysis, get_feedback
from ui import (
    console, 
    print_header, 
    print_success, 
    print_error, 
    print_warning,
    display_password_list,
    display_password_info,
    display_strength_bar,
    display_feedback,
    display_main_menu
)
import pyperclip


def setup_master_password():
    print_header("FIRST TIME SETUP")
    console.print("[cyan]Create a master password, this will be needed to access passwords[/cyan]")
    
    while True: 
        """BTW ------   switch from getpass.getpass to input to be able to see input"""
        input_password = getpass.getpass("Enter master password:  ")
        confirm_password = getpass.getpass("Confirm master password:  ")

        if input_password == confirm_password:
            if len(input_password) < 8:
                print_error("Password must be at least 8 characters")
                continue
            hashed_input = hash_password(input_password)
            save_master_password_hash(hashed_input)
            print_success("Master password created successfully")
            return True
        else:
            print_error("Passwords don't match, please try again")


def login():
    stored_hash = load_master_password_hash()
    att = 4

    while att > 0:
        print_header("LOGIN")
        password = getpass.getpass("Enter master password:  ")

        if verify_master_password(password, stored_hash):
            print_success("Access Granted!")
            return password
        else:
            att -= 1
            if att > 0:
                print_error(f"Incorrect password. {att} attempts remaining")
            else:
                print_error("Too many failed attempts, Goodbye.")
                exit()
    return None

def generate_password_menu():
    """generate a password, menu to do that"""
    print_header("GENERATE PASSWORD")

    try:
        length = int(input("Please enter a length (default = 16):       ") or 16)
        use_symbols = input("Would you like to use symbols? (y/n, default = y):        ").lower() != "n"

        password = generate_password(length, use_symbols)

        result = calculate_strength(password)
        console.print(f"\n[bold green]Generated password:[/bold green] {password}")
        display_strength_bar(result['score'], result['rating'])

        pyperclip.copy(password)
        print_success("Copied to clipboard!")
        
    except ValueError:
        print_error("Invalid length!")



def search_for_service(master_pass):
    entries = load_entries()

    print_header("SEARCH FOR PASSWORD")

    search_term = input("Enter a service name (E.G., git, youtube, gmail):  ").strip().lower()
    matches = []

    for entry in entries:
        if search_term in entry['service'].strip().lower():
            matches.append(entry)
    
    for i, entry in enumerate(matches, 1):
        print(f"{i}. {entry['service']} ({entry['username']})")
    
    try:
        choice = int(input("\nEnter your choice here: "))
    except ValueError:
        print_error("Please enter a valid number")
        return

    if choice < 1 or choice > len(matches):
        print_error("Invalid choice")
        return

    selected = matches[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    result = calculate_strength(decrypted_pass)
    display_password_info(selected, decrypted_pass, result)
    
    if result['score'] < 40 or result.get('is_common'):
        print_warning("This password is weak or commonly used!")
        show_tips = input("Show improvement suggestions? (y/n): ").lower()
        if show_tips == 'y':
            feedback = get_feedback(decrypted_pass)
            display_feedback(feedback)
    
    pyperclip.copy(decrypted_pass)
    print_success("Password copied to clipboard!")




def add_password(master_pass: str):
    print_header("ADD NEW PASSWORD")
    site = input("Service name (e.g., YouTube, Gmail, GitHub):  ").strip()
    username = input("Enter username/email: ").strip()

    gen_pass = input("Generate password? (y/n): ").lower()

    if gen_pass == "y":
        try:
            length = int(input("Length (default 16): ") or 16)
            use_symbols = input("Use symbols? (y/n, default y): ").lower() != "n"
            password = generate_password(length, use_symbols)
            
            # Show generated password with strength
            result = calculate_strength(password)
            console.print(f"\n[bold green]Generated:[/bold green] {password}")
            display_strength_bar(result['score'], result['rating'])
            pyperclip.copy(password)
            print_success("Copied to clipboard!")
        except ValueError:
            print_error("Invalid length, using default")
            password = generate_password()
    else:
        password = getpass.getpass("Password: ")
        
        # Analyze user's password
        result = calculate_strength(password)
        display_strength_bar(result['score'], result['rating'])
        
        # Warn if common or weak
        if result.get('is_common'):
            print_warning("This is a commonly used password!")
            feedback = get_feedback(password)
            display_feedback(feedback)
            confirm = input("\nSave anyway? (y/n): ").lower()
            if confirm != 'y':
                print_error("Password not saved")
                return
        elif result['score'] < 40:
            print_warning("This password is weak!")
            show_tips = input("Show improvement tips? (y/n): ").lower()
            if show_tips == 'y':
                feedback = get_feedback(password)
                display_feedback(feedback)
            confirm = input("\nSave anyway? (y/n): ").lower()
            if confirm != 'y':
                print_error("Password not saved")
                return

    if not site or not username or not password:
        print_error("All fields must be completed")
        return
    
    encrypted_password = encrypt_pass(password, master_pass)

    entries = load_entries()
    next_id_num = len(entries)+1

    new_entry = {
        'id': next_id_num,
        'service': site,
        'username': username,
        'password': encrypted_password,
        'created': datetime.now().strftime('%Y-%m-%d'),
        'strength': result['rating']
    }

    entries.append(new_entry)
    save_entries(entries)
    print_success(f"Password added for '{site}' successfully")

def get_password(master_pass: str):
    entries = load_entries()

    if len(entries) < 1:
        print_warning("No entries available")
        return
    print_header("RETRIEVE PASSWORD")

    view_type = console.input("[cyan]Search(1) or list all services(2)?[/cyan] ").strip()

    if view_type == "1":
        search_for_service(master_pass)
        return

    display_password_list(entries)

    try:
        choice = int(console.input("\n[cyan]Enter your choice:[/cyan] "))
    except ValueError:
        print_error("Please enter a valid number")
        return

    if choice < 1 or choice > len(entries):
        print_error("Invalid choice")
        return

    selected = entries[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    result = calculate_strength(decrypted_pass)
    display_password_info(selected, decrypted_pass, result)

    # Warn if weak
    if result['score'] < 40 or result.get('is_common'):
        print_warning("This password is weak or commonly used!")
        show_tips = input("Show improvement suggestions? (y/n): ").lower()
        if show_tips == 'y':
            feedback = get_feedback(decrypted_pass)
            display_feedback(feedback)
    
    pyperclip.copy(decrypted_pass)
    print_success("Password copied to clipboard!")

def delete_password():
    entries = load_entries()

    if len(entries) < 1:
        print_warning("No entries available")
        return
    
    print_header("DELETE PASSWORD")
    display_password_list(entries)

    try:
        choice = int(input("\nEnter your choice here: "))
    except ValueError:
        print_error("Please enter a valid number")
        return

    if choice < 1 or choice > len(entries):
        print_error("Invalid choice")
        return

    service_name = entries[choice-1]['service']
    confirm = console.input("[cyan]CONFIRM DELETE (y/n):[/cyan] ").lower()

    if confirm == "y":
        del entries[choice-1]
        save_entries(entries)
        print_success(f"Password for '{service_name}' deleted successfully!")

def update_password(master_pass: str):
    """Updates password"""
    entries = load_entries()

    if len(entries) < 1:
        print_warning("No entries available")
        return
    
    print_header("UPDATE PASSWORD")
    display_password_list(entries)

    try:
        choice = int(input("\nEnter your choice here: "))
    except ValueError:
        print_error("Please enter a valid number")
        return

    if choice < 1 or choice > len(entries):
        print_error("Invalid choice")
        return

    selected = entries[choice-1]
    decrypted_pass = decrypt_pass(selected['password'], master_pass)

    result = calculate_strength(decrypted_pass)
    display_password_info(selected, decrypted_pass, result)

    try:
        update_choice = int(input("Would you like to change your password(1), username(2) or both(3)?  "))
    except ValueError:
        print_error("INVALID")
        return
    
    new_username = selected['username']
    new_password = selected['password']  # Keep encrypted
    new_strength = selected.get('strength', 'unknown')

    if update_choice == 1:
        # Update password only
        password = getpass.getpass("Enter new password: ")
        if not password:
            print_error("Password cannot be empty")
            return
        new_password = encrypt_pass(password, master_pass)
        strength_result = calculate_strength(password)
        new_strength = strength_result['rating']
        
    elif update_choice == 2:
        # Update username only
        username = input("Enter new username: ").strip()
        if not username:
            print_error("Username cannot be empty")
            return
        new_username = username
        
    elif update_choice == 3:
        # Update both
        username = input("Enter new username: ").strip()
        password = getpass.getpass("Enter new password: ")
        if not username or not password:
            print_error("Fields cannot be empty")
            return
        new_username = username
        new_password = encrypt_pass(password, master_pass)
        strength_result = calculate_strength(password)
        new_strength = strength_result['rating']
        
    else:
        print_error("Invalid choice")
        return

    # Update the entry
    entries[choice - 1] = {
        'id': selected['id'],
        'service': selected['service'],
        'username': new_username,
        'password': new_password,
        'created': selected['created'],
        'strength': new_strength
    }

    save_entries(entries)
    print_success(f"Password for '{selected['service']}' updated successfully!")



def analyze_password_standalone():
    """Standalone password strength analyzer"""
    print_header("PASSWORD STRENGTH ANALYZER")
    password = getpass.getpass("Enter password to analyze: ")
    
    if not password:
        print_error("No password entered")
        return
    
    display_strength_analysis(password)




def main_menu(master_pass: str):
    running = True
    while running:
        display_main_menu()
        
        choice = console.input("\n[bold cyan]Enter choice:[/bold cyan] ").strip()

        if choice == "1":
            add_password(master_pass)
        elif choice == "2":
            get_password(master_pass)
        elif choice == "3":
            update_password(master_pass)
        elif choice == "4":
            delete_password()
        elif choice == "5":
            analyze_password_standalone()
        elif choice == "6":
            print_success("Goodbye! 👋")
            running = False
        else:
            print_error("Invalid choice - please enter 1-6")


def main():
    console.print("\n[bold cyan]🔐 PASSWORD MANAGER[/bold cyan]\n", justify="center")

    stored_hash = load_master_password_hash()

    if not stored_hash:
        setup_master_password()
        master_pass = login()
    else:
        master_pass = login()

    print_success("Welcome to your Password Manager!")

    main_menu(master_pass)

if __name__ == "__main__":
    main()