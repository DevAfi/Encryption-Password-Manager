## Password Manager CLI

### Overview
A comprehensive, local-first password manager you run from the terminal. Features include:
- **Master password authentication**
- **Add new password entries**
- **Retrieve/view passwords**
- **Search passwords by service**
- **Update existing passwords**
- **Delete password entries**
- **Password generation with customizable options**
- **Password strength analysis**
- **Copy passwords to clipboard**
- **Basic encryption**
- **Local JSON storage**

This repo includes a complete CLI with all essential password management features.

### Tech Stack
- **Python**
- **cryptography (Fernet)**: symmetric encryption for stored secrets
- **getpass**: secure terminal input
- **json**: local storage
- **hashlib/PBKDF2**: master password hashing/derivation
- Optional: **pyperclip** for clipboard copy, **argparse/click** for CLI UX

### Current Status ✅ FULLY FEATURED
- ✅ Master password authentication with secure hashing
- ✅ Add new password entries with encryption
- ✅ Retrieve/view passwords with decryption
- ✅ Search passwords by service name
- ✅ Update existing password entries
- ✅ Delete password entries
- ✅ Password generation with customizable options
- ✅ Password strength analysis and feedback
- ✅ Copy passwords to clipboard
- ✅ Local JSON storage with encrypted data
- ✅ Interactive CLI menu system
- ✅ Secure password input using getpass

### Project Structure
```text
password_manager/
  config.json           # stores master password hash (or KDF params)
  data.json             # encrypted entries (ciphertext + metadata)
  crypto.py             # hashing and Fernet encryption helpers
  storage.py            # config and data file read/write helpers
  password_analyzer.py  # password strength analysis and common password checking
  common_passwords.txt  # list of common passwords for strength analysis
  main.py               # CLI entrypoint with full feature set
  README.md
  venv/                 # local virtual environment (optional)
```

### Security Model (MVP)
- A master password is required to unlock the vault.
- The master password is never stored in plaintext.
- Entries are stored encrypted at rest.
- Everything is local-only by default.

Notes:
- For strong security, use **PBKDF2** or **scrypt** with salt to derive a key from the master password, then use **Fernet** (AES-128 + HMAC) for entry encryption. Avoid raw SHA-256 for password hashing in production.

### Getting Started

#### 1) Requirements
- Python 3.10+
- Windows/macOS/Linux supported. You’re on Windows 10.

#### 2) Create and activate a virtual environment (optional but recommended)
```bash
# from project root
python -m venv venv

# Windows PowerShell
./venv/Scripts/Activate.ps1
# or Command Prompt
venv\Scripts\activate.bat
# or Git Bash
source venv/Scripts/activate
```

#### 3) Install dependencies
```bash
pip install cryptography pyperclip
```

### Usage
Run the password manager from the project root:
```bash
python main.py
```

#### First Time Setup
- The application will automatically detect if no master password exists
- You'll be prompted to create a master password (minimum 8 characters)
- Password is securely hashed and stored in `config.json`

#### Main Menu Options
1. **Add a new password** - Store encrypted credentials for any service
2. **Retrieve a password** - View stored passwords by selecting from a list
3. **Search passwords** - Find passwords by service name
4. **Update password** - Modify existing password entries
5. **Delete password** - Remove password entries
6. **Generate password** - Create secure passwords with custom options
7. **Analyze password strength** - Check password security and get feedback
8. **Exit** - Close the application

#### Security Features
- Master password verification with 4-attempt limit
- All passwords encrypted using Fernet (AES-128 + HMAC)
- PBKDF2 key derivation with 100,000 iterations
- Secure password input (hidden characters)
- Local-only storage (no cloud dependencies)
- Password strength analysis against common passwords
- Secure password generation with customizable parameters

### Configuration Files
- `config.json`: master password hash and/or KDF metadata (salt, iterations). Never stores plaintext.
- `data.json`: encrypted entries. Do not edit by hand.
- `common_passwords.txt`: list of common passwords used for strength analysis (contains offensive content - see disclaimer below)

### Roadmap (Future Enhancements)
- **Phase 2: Advanced Features** 🔄
  - Auto-lock after inactivity
  - Expiry warnings for passwords
  - Encrypted import/export functionality
- **Phase 3: Polish & UX** 🔄
  - Colored output with `rich`
  - Help documentation
  - Unit tests and CI
  - README visuals (demo GIFs)
  - Improved CLI UX and input validation

### Development Notes
- Run with:
```bash
python main.py
```
- Follow the code style and keep variables descriptive.
- Prefer early returns and minimal nesting.
- Avoid catching exceptions without meaningful handling.
- Uses PBKDF2 with SHA-256 and 100,000 iterations for key derivation
- Fernet encryption provides authenticated encryption (AES-128 + HMAC)

### Troubleshooting
- If `cryptography` fails to install, ensure build tools are present and Python is 64-bit.
- If clipboard copy fails, install `pyperclip` and ensure a compatible backend exists on your OS.
- If you forget the master password, there’s no recovery by design. Keep backups.

### Backup & Restore (planned)
- Add `backup`/`restore` commands to export/import an encrypted archive containing `config.json` + `data.json`.

### ⚠️ Content Warning

**Disclaimer**: The `common_passwords.txt` file contains passwords scraped from various web sources and includes offensive language, profanity, and slurs. This file is used solely for password strength analysis to help users avoid weak passwords. The offensive content is not endorsed by the project maintainers and is included only for security purposes. If you find this content inappropriate, you may delete or replace the file with a sanitized version.

### License
MIT