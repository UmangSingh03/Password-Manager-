🔐 Password Manager (Python + Tkinter)

A secure, desktop-based Password Manager built using Python, Tkinter, bcrypt, and JSON.
The application allows users to safely store, search, copy, and manage credentials with a master password–protected login system and an intuitive graphical interface.

🚀 Features

🔑 Master Password Authentication

First-time setup creates a hashed master password

Uses bcrypt for secure password hashing

⏳ Auto Session Timeout

Automatically closes the app after inactivity for enhanced security

🗂 Password Vault

Store website, username/email, and password

Data persisted in a local JSON file

🔍 Search Functionality

Instantly search saved credentials by website or username

👁 Show / Hide Password

Toggle visibility of stored passwords

📋 One-Click Copy

Copy passwords securely to clipboard

🗑 Delete Passwords

Remove credentials with instant UI refresh

🎨 Modern GUI

Clean, dark-themed UI using Tkinter

Scrollable dashboard with card-based layout

🛠 Tech Stack

Language: Python

GUI: Tkinter

Security: bcrypt (password hashing)

Storage: JSON (local file-based storage)

📂 Project Structure
password-manager/
│
├── main.py          # Main application file
├── vault.json       # Stores encrypted password records
├── master.hash      # Stores hashed master password
└── README.md

🔒 Security Details

Master password is never stored in plain text

Uses bcrypt hashing with salt

Automatic logout on inactivity

Passwords are masked by default in the UI

⚠️ Note: Passwords are stored in plain text inside vault.json.
Future versions can add encryption (e.g., Fernet/AES) for enhanced security.

▶️ How to Run

Clone the repository

git clone https://github.com/your-username/password-manager.git
cd password-manager


Install dependencies

pip install bcrypt


Run the application

python main.py


First Launch

Set a master password

Restart and log in using the same password
