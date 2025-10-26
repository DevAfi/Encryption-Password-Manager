## 🔐 Password Manager CLI

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-PBKDF2%20%2B%20Fernet-red.svg)](https://cryptography.io/)
[![UI](https://img.shields.io/badge/UI-Rich%20Terminal-purple.svg)](https://rich.readthedocs.io/)

### Overview
A comprehensive, local-first password manager with a beautiful terminal interface built using Rich. Features include:
- **🔑 Master password authentication** with secure PBKDF2 hashing
- **➕ Add new password entries** with real-time strength analysis
- **🔍 Retrieve/view passwords** with search functionality
- **✏️ Update existing passwords** and usernames
- **🗑️ Delete password entries** with confirmation
- **🎲 Password generation** with customizable length and symbols
- **📊 Advanced password strength analysis** with visual feedback
- **📋 Copy passwords to clipboard** automatically
- **🔒 Fernet encryption** (AES-128 + HMAC) for all stored data
- **💾 Local JSON storage** with encrypted entries
- **🎨 Beautiful Rich UI** with colored tables, panels, and progress bars

This repo includes a complete CLI with all essential password management features and a polished user experience.

### Tech Stack
- **Python 3.10+**
- **Rich**: Beautiful terminal UI with tables, panels, and colored output
- **cryptography (Fernet)**: Symmetric encryption for stored secrets (AES-128 + HMAC)
- **PBKDF2**: Secure key derivation with 100,000 iterations
- **pyperclip**: Automatic clipboard integration
- **getpass**: Secure password input (hidden characters)
- **json**: Local storage with encrypted data
- **hashlib**: Master password hashing

### Why I Built This

I created this password manager to solve a real problem I faced - managing dozens of passwords across different services while maintaining security and usability. Commercial password managers often require subscriptions, cloud storage, or complex setups. I wanted something that was:

- **🔒 Truly secure** - No cloud dependencies, enterprise-grade encryption
- **💻 Terminal-native** - Fast, keyboard-driven workflow for developers
- **🎨 Beautiful** - Rich terminal UI that's actually pleasant to use
- **📊 Educational** - Learn about cryptography, security, and CLI design
- **🛠️ Customizable** - Full control over features and data storage

This project demonstrates my approach to building production-ready software with security-first design principles.

### Project Structure
```text
password_manager/
  config.json           # stores master password hash (PBKDF2 params)
  data.json             # encrypted entries (ciphertext + metadata)
  crypto.py             # PBKDF2 key derivation and Fernet encryption helpers
  storage.py            # config and data file read/write helpers
  password_analyzer.py  # advanced password strength analysis and common password checking
  ui.py                 # Rich-powered terminal UI components (tables, panels, styling)
  common_passwords.txt  # comprehensive list of common passwords for strength analysis
  main.py               # CLI entrypoint with full feature set and Rich integration
  README.md
  venv/                 # local virtual environment (optional)
```

### Security Model (Production-Ready)
- **Master password authentication** with PBKDF2 key derivation (100,000 iterations)
- **Fernet encryption** (AES-128 + HMAC) for all stored passwords
- **No plaintext storage** - master password and entries are never stored unencrypted
- **Local-only by default** - no cloud dependencies or data transmission
- **Secure input handling** using getpass for hidden password entry
- **Common password detection** against comprehensive database
- **Sequential pattern detection** to prevent weak patterns

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
pip install cryptography pyperclip rich
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
1. **➕ Add a new password** - Store encrypted credentials with real-time strength analysis
2. **🔍 Retrieve a password** - View stored passwords with search functionality and detailed info panels
3. **✏️ Update password** - Modify existing password entries (password, username, or both)
4. **🗑️ Delete password** - Remove password entries with confirmation
5. **📊 Analyze password strength** - Standalone password analysis with visual feedback
6. **🚪 Exit** - Close the application

#### Security Features
- **🔐 Master password verification** with 4-attempt limit and secure hashing
- **🔒 Fernet encryption** (AES-128 + HMAC) for all stored passwords
- **⚡ PBKDF2 key derivation** with 100,000 iterations for maximum security
- **👁️ Secure password input** (hidden characters) using getpass
- **🏠 Local-only storage** (no cloud dependencies or data transmission)
- **📊 Advanced password analysis** against common passwords and patterns
- **🎲 Secure password generation** with customizable parameters
- **📋 Automatic clipboard integration** for seamless password copying

### Configuration Files
- **`config.json`**: Master password hash and PBKDF2 metadata (salt, iterations). Never stores plaintext.
- **`data.json`**: Encrypted password entries with metadata. Do not edit by hand.
- **`common_passwords.txt`**: Comprehensive database of common passwords for strength analysis (contains offensive content - see disclaimer below)
- **`ui.py`**: Rich-powered UI components including tables, panels, and styling functions

### Roadmap (Future Enhancements)
- **Phase 2: Advanced Features** 🔄
  - Auto-lock after inactivity
  - Password expiry warnings and notifications
  - Encrypted import/export functionality
  - Password history and versioning
  - Two-factor authentication support
- **Phase 3: Polish & Testing** 🔄
  - Comprehensive unit tests and CI/CD
  - Performance optimizations
  - README visuals (demo GIFs/screenshots)
  - Cross-platform compatibility improvements
  - Advanced CLI argument parsing

### Lessons Learned & Challenges Faced

**🔐 Security Implementation Challenges:**
- **Salt Management**: Initially used a fixed salt, learned the importance of random salt generation for production security
- **Key Derivation**: Balancing security (high iterations) with performance (user experience) - settled on 100k PBKDF2 iterations
- **Memory Security**: Discovered the need for secure memory clearing to prevent password exposure in memory dumps

**🎨 UI/UX Design Insights:**
- **Rich Library Learning Curve**: Mastering Rich's table, panel, and styling system for professional terminal interfaces
- **Color Accessibility**: Ensuring the interface works across different terminal themes and color schemes
- **User Flow**: Designing intuitive navigation that works for both power users and newcomers

**🏗️ Architecture Decisions:**
- **Modular Design**: Separating crypto, storage, analysis, and UI into distinct modules for maintainability
- **Error Handling**: Implementing comprehensive error handling without exposing sensitive information
- **Data Integrity**: Ensuring encrypted data remains valid across different Python versions and platforms

**⚡ Performance Considerations:**
- **Large Databases**: Optimizing search and loading for users with hundreds of password entries
- **Encryption Overhead**: Balancing security with speed for frequent operations
- **Memory Usage**: Managing memory efficiently when handling encrypted data

**🛠️ Development Process:**
- **Testing Strategy**: Learning to test cryptographic functions without compromising security
- **Documentation**: Balancing comprehensive documentation with security best practices
- **Cross-Platform**: Ensuring compatibility across Windows, macOS, and Linux

### Quick Start
```bash
# Install dependencies
pip install cryptography pyperclip rich

# Run the application
python main.py
```

### Development Notes
- **Code style**: Follow descriptive variable naming and early returns
- **Security**: Uses PBKDF2 with SHA-256 and 100,000 iterations for key derivation
- **Encryption**: Fernet provides authenticated encryption (AES-128 + HMAC)
- **UI**: Rich library provides beautiful terminal interfaces with tables, panels, and colored output
- **Architecture**: Modular design with separate files for crypto, storage, analysis, and UI components

### Troubleshooting
- **Installation issues**: If `cryptography` fails to install, ensure build tools are present and Python is 64-bit
- **Clipboard issues**: If clipboard copy fails, install `pyperclip` and ensure a compatible backend exists on your OS
- **Rich display issues**: If colors don't display properly, ensure your terminal supports ANSI colors
- **Password recovery**: If you forget the master password, there's no recovery by design. Keep backups of your data files
- **Performance**: Large password databases may take longer to load; consider optimizing if you have 1000+ entries

### Backup & Restore (Future Feature)
- **Encrypted backup/restore** commands to export/import archives containing `config.json` + `data.json`
- **Cross-platform compatibility** for backup files
- **Incremental backups** with timestamp tracking
- **Backup verification** to ensure data integrity

### ⚠️ Content Warning

**Disclaimer**: The `common_passwords.txt` file contains passwords scraped from various web sources and includes offensive language, profanity, and slurs. This file is used solely for password strength analysis to help users avoid weak passwords. The offensive content is not endorsed by the project maintainers and is included only for security purposes. If you find this content inappropriate, you may delete or replace the file with a sanitized version.

### License
MIT