## Password Manager CLI

### Overview
A minimal, local-first password manager you run from the terminal. Focused on a secure MVP:
- **Master password authentication**
- **Add new password entries**
- **Retrieve/view passwords**
- **Basic encryption**
- **Local JSON storage**

This repo also includes a roadmap for growing into a fuller CLI with generation, clipboard, search, update/delete, and backups.

### Tech Stack
- **Python**
- **cryptography (Fernet)**: symmetric encryption for stored secrets
- **getpass**: secure terminal input
- **json**: local storage
- **hashlib/PBKDF2**: master password hashing/derivation
- Optional: **pyperclip** for clipboard copy, **argparse/click** for CLI UX

### Current Status (MVP) ✅ COMPLETED
- ✅ Master password authentication with secure hashing
- ✅ Add new password entries with encryption
- ✅ Retrieve/view passwords with decryption
- ✅ Local JSON storage with encrypted data
- ✅ Interactive CLI menu system
- ✅ Secure password input using getpass

### Project Structure
```text
password_manager/
  config.json           # stores master password hash (or KDF params)
  data.json             # encrypted entries (ciphertext + metadata)
  crypto.py             # hashing and (soon) Fernet encryption helpers
  storage.py            # config and data file read/write helpers
  main.py               # CLI entrypoint (commands: init, add, get, list ...)
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
3. **Exit** - Close the application

#### Security Features
- Master password verification with 4-attempt limit
- All passwords encrypted using Fernet (AES-128 + HMAC)
- PBKDF2 key derivation with 100,000 iterations
- Secure password input (hidden characters)
- Local-only storage (no cloud dependencies)

### Configuration Files
- `config.json`: master password hash and/or KDF metadata (salt, iterations). Never stores plaintext.
- `data.json`: encrypted entries. Do not edit by hand.

### Roadmap (Future Enhancements)
- **Phase 2: Password Generation** 🔄
  - Secure generator (length, symbols, numbers, case options)
  - Strength checker
  - Integrate into `add` flow
- **Phase 3: Enhanced Features** 🔄
  - Search/filter entries
  - Update/delete entries
  - Copy to clipboard
- **Phase 4: Security & UX** 🔄
  - Auto-lock after inactivity
  - Expiry warnings
  - Encrypted import/export
  - Improved CLI UX and input validation
- **Phase 5: Polish** 🔄
  - Colored output with `rich`
  - Help docs
  - Unit tests and CI
  - README visuals (demo GIFs)

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

### License
MIT