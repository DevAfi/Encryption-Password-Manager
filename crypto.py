import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def hash_password(password: str) -> str:
    """ Hashes a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_master_password(entered_pass: str, stored_hash: str) -> bool:
    hashed_input = hash_password(entered_pass)
    return hashed_input == stored_hash

def generatekey(master_pass: str) -> bytes:
    salt = b'password_manager_salt_2025'
    # FOR NOW -- I use a fixed salt, in actual production ima generate a random salt and store it

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000, #Kinda high, ill adjust later
    )
    key=base64.urlsafe_b64encode(kdf.derive(master_pass.encode()))
    return key

def encrypt_pass(norm_pass: str, master_pass: str) -> str:
    key = generatekey(master_pass)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(norm_pass.encode())
    return encrypted.decode() #to store in json
def decrypt_pass(enc_pass: str, master_pass: str) -> str:
    key = generatekey(master_pass)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(enc_pass.encode())
    return decrypted.decode() 