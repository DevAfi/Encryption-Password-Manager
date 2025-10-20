import hashlib

def hash_password(password: str) -> str:
    """ Hashes a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_master_password(entered_pass: str, stored_hash: str) -> bool:
    hashed_input = hashlib.sha256(entered_pass)
    return entered_pass == stored_hash