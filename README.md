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

### 1. Clone the Repository

```bash
git clone [https://github.com/maramatef111/Online-Library-System-.git](https://github.com/maramatef111/Online-Library-System-.git)
cd Online-Library-System
```

### 2. Create and Activate a Virtual Environment
   
  ON Windows

```bash
  python -m venv venv
venv\Scripts\activate
 ```

### 3. Install Required Packages

```bash

pip install -r requirements.txt
```


### 4. Run the Application

```
python main.py
```
Open your browser and go to:
 http://127.0.0.1:5000
 From there, you can:
 
 - View the home page

- Log in or sign up

- Browse and borrow books

- Access the admin dashboard (if admin user)

### 5. Frontend (FE) Setup 
The frontend of this project is built using Flask templates (HTML, CSS).
All the user interfaces are located inside:

```
website/templates/   → contains HTML pages  
website/static/      → contains CSS and static files
```
Once the Flask server is running, you can access the frontend directly in your browser.

### 6. Login Credentials (Seeded Data)

| Role  | Email                                         | Password |
| ----- | --------------------------------------------- | -------- |
| Admin | [admin@example.com](mailto:admin@example.com) | admin123 |
| User  | [maram@example.com](mailto:maram@example.com) | password |


## Website 

![image alt](https://github.com/maramatef111/Online-Library-System-/blob/0cbdca2dc6f8c54046c1a63d724ea48e9c0fd988/Admin%20Dashboard.png)

![image alt](https://github.com/maramatef111/Online-Library-System-/blob/7c509ead29e0e288d5a91045d7220028e96a5edc/My%20Borrows%20admin.png)

![image alt](https://github.com/maramatef111/Online-Library-System-/blob/7c509ead29e0e288d5a91045d7220028e96a5edc/signup.png)

![image alt](https://github.com/maramatef111/Online-Library-System-/blob/7c509ead29e0e288d5a91045d7220028e96a5edc/user_books.png)


![image alt](https://github.com/maramatef111/Online-Library-System-/blob/7c509ead29e0e288d5a91045d7220028e96a5edc/User%20borrows.png)
















