import os
import json

def save_master_password_hash(pass_hash: str):
    """"""
    config = {'master_password_hash': pass_hash}
    with open('config.json', 'w') as f:
        json.dump(config, f)

def load_master_password_hash() -> str:
    """Load the master password hash from config"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('master_password_hash', '')
    except (FileNotFoundError, json.JSONDecodeError):
        return ''