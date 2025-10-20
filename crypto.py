import hashlib

def hash_password(password: str) -> str:
    """ Hashes a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_master_password(entered_pass: str, stored_hash: str) -> bool:
    hashed_input = hash_password(entered_pass)
    return hashed_input == stored_hash