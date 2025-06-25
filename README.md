🔐 Secure Account & Credential Manager
A responsive Account Manager Web App built using HTML, CSS, JavaScript, and Python (Flask) that allows you to securely add, manage, and view account credentials like passwords, API keys, and tokens.

🧰 Tech Stack Used:
Layer	Technology
Frontend	HTML5, CSS3, Bootstrap 5, JavaScript
Backend	Python (Flask Framework)
Database	SQLite / MongoDB Atlas
Security	AES-256 Encryption, JWT Authentication, 2FA (Email-based)

✨ Features:
✅ User Registration & Login
✅ Master Password Protection
✅ Account Credential Storage
✅ AES-256 Encrypted Password Saving
✅ Password Strength Checker (Frontend JS)
✅ View, Edit, Delete Credentials
✅ Dashboard with Login History & Features
✅ Dark/Light Mode Toggle
✅ Responsive UI (Mobile-Friendly)

📌 Project Folder Structure:
bash
Copy
Edit
/account-manager
├── app.py                  # Flask Backend
├── templates/              # HTML Files (Dashboard, Login, Register, etc)
├── static/
│   ├── css/                # Custom CSS
│   └── js/                 # JS Files
├── database/               # SQLite DB (or MongoDB connection)
├── requirements.txt        # Python Dependencies
└── README.md               # Project Readme
🖥️ Screens Included:
Page	Description
Dashboard	View features and login history
Add Credentials	Add new account credentials
Login	User login with master password
Register	User signup with password strength check
Forgot Password	Reset your password securely

🚀 How to Run This Project Locally:
✅ 1. Clone this Repository:
bash
Copy
Edit
git clone https://github.com/yourusername/account-manager.git
✅ 2. Set up Virtual Environment & Install Dependencies:
bash
Copy
Edit
cd account-manager
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
✅ 3. Run Flask App:
bash
Copy
Edit
python app.py
Then visit:
📡 http://127.0.0.1:5000/

📝 Live Demo / Project Link:
🌐 👉 Click Here for Live Demo
(If deployed on Render, Heroku, or Replit)

📷 Screenshots:
Dashboard	Add Credentials

🔒 Security Note:
All user passwords and stored credentials are AES-256 encrypted with PBKDF2 master key derivation. Additionally, JWT and email-based 2FA add extra protection.

🤝 Contributing:
Fork this repository 🍴


📧 Contact:
For help or queries:
📧 Email: support@securevault.com
🌐 Website: https://yourwebsite.com

