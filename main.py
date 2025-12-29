# Created by: Izram Khan
# Date completed: 29-Dec-2025
#____________________________________________________________________________________________________
import hashlib
import base64
from cryptography.fernet import Fernet
import os
import string
from datetime import datetime

def is_strong_master_password(password):
    if len(password) < 12:
        return False
    
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_special_chars = any(c in string.punctuation for c in password)

    return has_lower and has_upper and has_digit and has_special_chars

def create_master_file():
    while True:
        master_password = input('\nCreate a strong master password: ')

        if not is_strong_master_password(master_password):
            print(
                    "\n❌ Weak password.\n\n"
                    "Requirements:\n"
                    "- At least 12 characters\n"
                    "- Uppercase + lowercase\n"
                    "- Atleast one number\n"
                    "- Atleast one special character"
            )
            continue

        master_hash = hashlib.sha256(master_password.encode()).hexdigest()
        with open('master.hash', 'w') as f:
            f.write(master_hash)
        print(f'\n✅ Master password created successfully! Do not forget it!')
        break

def verify_master_file(master_password):
    password_hash = hashlib.sha256(master_password.encode()).hexdigest()
    with open('master.hash', 'r') as f:
        saved_hash = f.read()
    return password_hash == saved_hash

def get_fernet(master_password):
    '''Fernet key will be created from master password'''
    key = base64.urlsafe_b64encode(hashlib.sha256(master_password.encode()).digest())
    return Fernet(key)

def change_master_password():
    old_password = input('\nEnter the old password: ')
    
    if not verify_master_file(old_password):
        print('\n❌ Error: Incorrect master password!')
        return

    while True:
        new_password = input('\nEnter NEW password: ')
        if not is_strong_master_password(new_password):
            print('\n❌ Error: Weak Password! Try again!')
            continue
        break

    old_f = get_fernet(old_password)
    new_f = get_fernet(new_password)

    if not os.path.exists('vault.txt'):
        print('\n❌ Error: No password exists to encrypt!') 
    else:
        updated_lines = []

        with open('vault.txt', 'r') as file:
            for line in file:
                site, username, encrypted = line.strip().split('|')
                decrypted = old_f.decrypt(encrypted.encode()).decode()
                new_encrypted = new_f.encrypt(decrypted.encode()).decode()
                updated_lines.append(f'{site} | {username} | {new_encrypted}\n')

        with open('vault.txt', 'w') as file:
            file.writelines(updated_lines)

    # Making new hash
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    with open('master.hash', 'w') as f:
        f.write(new_hash)
    
    print('\n✅ Master password changed successfully!')

def add_password(f):
    '''Encrypt and save a password to the vault file.'''
    site = input('\nEnter site name: ')
    username = input('\nEnter username: ')

    passowrd = input('\nEnter the password: ')
    encrypted = f.encrypt(passowrd.encode())

    # Save passwords to vault.txt
    with open('vault.txt', 'a') as file:
        file.write(f'{site.upper()} | {username} | {encrypted.decode()}\n')
    print('\n✅ Password saved!')

def delete_password(f):
    """Delete a saved password from the vault."""
    if not os.path.exists('vault.txt'):
        print("\nNo passwords saved yet!")
        return

    site_to_delete = input("\nEnter the site name of the password to delete: ").upper()
    username_to_delete = input("Enter the username of the password to delete: ")

    lines_kept = []
    deleted = False

    with open('vault.txt', 'r') as file:
        for line in file:
            if not line.strip():
                continue
            # Each line is 'SITE | USERNAME | ENCRYPTED_PASSWORD'
            parts = line.strip().split(' | ')
            if len(parts) != 3:
                continue
            site, username, encrypted = parts

            # Keep all lines except the one to delete
            if site.upper() == site_to_delete and username == username_to_delete:
                deleted = True
            else:
                lines_kept.append(line)

    if deleted:
        # Overwrite vault.txt with remaining lines
        with open('vault.txt', 'w') as file:
            file.writelines(lines_kept)
        print("\n✅ Password deleted successfully!")
    else:
        print("\n❌ No matching password found.")

def view_passwords(f):
    '''Decrypt and show all saved passwords.'''
    if not os.path.exists('vault.txt'):
        print('\nNo passwords saved yet!')
        return

    with open('vault.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # Split only for display purposes
            parts = line.split(' | ')
            if len(parts) != 3:
                print(f"\n❌ Malformed line found: {line}")
                continue
            site, username, encrypted = parts
            decrypted = f.decrypt(encrypted.encode()).decode()
            print(f'\nSite: {site}\nUsername: {username}\nPassword: {decrypted}')

def get_current_time():
    return datetime.now()

def check_auto_lock(last_action_time, timeout=300):

    current_time = get_current_time()
    inactive_time = (current_time - last_action_time).total_seconds()

    if inactive_time > timeout:
        print('\n🛑 Vault locked due to longer inactivity (5 min)!')
        return True
    
    return False

def main_func():
    if not os.path.exists('master.hash'):
        create_master_file()
    
    else:
        master_password = input('\nEnter the master password to verify: ')

        if verify_master_file(master_password):
            f = get_fernet(master_password)
            print('\n✅ Vault unlocked!')
            last_action_time = get_current_time()

            while True:
                action = input(
                    "\n| add | view | delete | change-master | exit |: "
                    ).lower()
                
                if check_auto_lock(last_action_time):
                    break
                
                if action == 'add':
                    add_password(f)
                    last_action_time = get_current_time()

                elif action == 'view':
                    view_passwords(f)
                    last_action_time = get_current_time()

                elif action == 'delete':
                    delete_password(f)
                    last_action_time = get_current_time()

                elif action == 'change-master':
                    change_master_password()
                    break

                elif action == 'exit':
                    print('\n🛑 Vault Locked!')
                    break

                else:
                    print('\n❌ Invalid action!')

        else:
            print('\n❌ Wrong master password. Access denied!')

if __name__ == '__main__':
    main_func()

#____________________________________________________________________________________________________