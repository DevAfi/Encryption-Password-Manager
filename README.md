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

### Current Status (MVP)
- Project scaffolded with core modules.
- Master password hashing and config storage in progress.
- CLI commands will follow the usage below as they land.

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
Run commands from the project root. Examples assume:
```bash
python main.py <command> [options]
```

#### Initialize vault and set master password
```bash
python main.py init
```
- Prompts securely for a master password.
- Stores a hash/KDF parameters in `config.json`.
- Creates an empty `data.json` if missing.

#### Add a new password entry
```bash
python main.py add --service github --username yourname
# will prompt securely for the password (or generate in future phases)
```
- Encrypts and stores the entry in `data.json`.

#### Retrieve/view a password
```bash
python main.py get --service github
# prompts for master password, then prints or offers to copy to clipboard
```

#### List stored services (metadata only)
```bash
python main.py list
```
- Shows service names and usernames (no plaintext passwords).

### Configuration Files
- `config.json`: master password hash and/or KDF metadata (salt, iterations). Never stores plaintext.
- `data.json`: encrypted entries. Do not edit by hand.

### Roadmap (Phased Plan)
- **Phase 1: Core Foundation**
  - Master password creation & verification
  - Fernet encryption/decryption
  - Add/retrieve entries, encrypted JSON storage
- **Phase 2: Password Generation**
  - Secure generator (length, symbols, numbers, case options)
  - Strength checker
  - Integrate into `add` flow
- **Phase 3: Enhanced Features**
  - List/search/filter
  - Update/delete entries
  - Copy to clipboard
- **Phase 4: Security & UX**
  - Auto-lock after inactivity
  - Expiry warnings
  - Encrypted import/export
  - Improved CLI UX and input validation
- **Phase 5: Polish**
  - Colored output with `rich`
  - Help docs
  - Unit tests and CI
  - README visuals (demo GIFs)

### Development Notes
- Run with:
```bash
python main.py --help
```
- Follow the code style and keep variables descriptive.
- Prefer early returns and minimal nesting.
- Avoid catching exceptions without meaningful handling.

### Troubleshooting
- If `cryptography` fails to install, ensure build tools are present and Python is 64-bit.
- If clipboard copy fails, install `pyperclip` and ensure a compatible backend exists on your OS.
- If you forget the master password, there’s no recovery by design. Keep backups.

### Backup & Restore (planned)
- Add `backup`/`restore` commands to export/import an encrypted archive containing `config.json` + `data.json`.

### License
MIT