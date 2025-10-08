# Online Library System

A Flask-based web application for managing library resources, borrowing, and returning books. Includes user authentication (Flask sessions) and API access (JWT authentication). Admin users can manage books through a dedicated dashboard.

---

## Features

### web interface 
- 📖 Browse available books with search by title or author
- 📥 Borrow books via web forms (session-based)
- 📤 Return books via web forms
- 👩‍💻 Admin dashboard to add, edit, or delete books
- 🔐 User authentication (login/signup/logout)
- ⚡ Friendly UI 

### API (JWT-based)
- Get JWT token for authentication
- List all books
- Borrow books via API
- Return borrowed books via API

---

## Setup Instructions

To run this project locally, follow these steps:

1. **Clone the repository**
```bash
git clone https://github.com/maramatef111/Online-Library-System-.git
cd Online-Library-System

2. **Create and Activate a Virtual Environment**

  ON Windows 
```bash
  python -m venv venv
venv\Scripts\activate

3. **Install Required Packages**

```bash
pip install -r requirements.txt

4. **Run the Application**

```bash
python main.py







