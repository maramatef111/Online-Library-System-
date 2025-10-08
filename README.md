# Online Library System

A Flask-based web application for managing library resources, borrowing, and returning books. Includes user authentication (Flask sessions) and API access (JWT authentication). Admin users can manage books through a dedicated dashboard.

---

## Features

- User Authentication: Login, signup, and logout.

- Book Management: Admin can add, edit, or delete books.

- Borrowing System: Users can borrow and return books easily.

- JWT Token API: Secure API access for external requests.

- SQLite Database: Simple and portable database for development.

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
venv\Scripts\activate ```

3. **Install Required Packages**

```bash

pip install -r requirements.txt 


4. **Run the Application**

```
pip install -r requirements.txt
```


5. **Login Credentials (Seeded Data)**

| Role  | Email                                         | Password |
| ----- | --------------------------------------------- | -------- |
| Admin | [admin@example.com](mailto:admin@example.com) | admin123 |
| User  | [maram@example.com](mailto:maram@example.com) | password |







