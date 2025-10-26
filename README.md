# Flask Base Project

A starter project for building RESTful APIs and web applications with **Flask**, featuring PostgreSQL integration, email notifications, JWT authentication, and Google OAuth2 support.

---

## Table of Contents

* [Project Setup](#project-setup)
* [Environment Variables](#environment-variables)
* [Database Setup](#database-setup)
* [Running the Application](#running-the-application)
* [Move Default Avatar](#move-default-avatar)
* [Default Admin User](#default-admin-user)
* [Dependencies](#dependencies)
* [License](#license)

---

## Project Setup

After cloning the repository:

```bash
git clone <this-repo-url>
cd flask_base_project
```

### 1. Create a Python virtual environment

```bash
python -m venv venv
```

Activate it:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux / macOS:**

```bash
source venv/bin/activate
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Before running the app, ensure you have **PostgreSQL** installed and running.

Create a `.env` file under:

```
app/commons/const/const/.env
```

Populate it with the following entries (replace the placeholders with your actual values):

```ini
# Debug mode
debug_status = 1

# PostgreSQL database URI
data_base_uri = 'postgresql://<db_user>:<db_password>@localhost:5432/<db_name>'

# SMTP configuration for email notifications
smtp_server = "<smtp_server>"
smtp_port = <smtp_port>
smtp_user = "<smtp_user_email>"
smtp_password = "<smtp_user_password>"

# Default admin user
admin_user_firstname = "<admin_firstname>"
admin_user_lastname = "<admin_lastname>"
admin_username = "<admin_username>"
admin_user_email = "<admin_email>"
admin_user_password = "<admin_password>"

# Application secrets
app_secret_key = "<app_secret_key>"
jwt_secret_key = "<jwt_secret_key>"

# External APIs
x_rapidapi_host = "<rapidapi_host>"
x_rapidapi_key = "<rapidapi_key>"

# Google OAuth2 credentials
oauth_client_id = "<google_client_id>"
oauth_client_secret = "<google_client_secret>"
oauth_redirect_uri = "<redirect_uri>"
```

> **Note:** Ensure `.env` file is kept private and not committed to version control.

---

## Database Setup

1. Make sure PostgreSQL is installed and running.
2. Create a database for the application (example):

```sql
CREATE DATABASE flask_base_db;
```

3. Update `data_base_uri` in `.env` file with the correct username, password, and database name.

---

## Running the Application

Once the virtual environment is activated and dependencies installed, run the Flask application:

```bash
python app/__init__.py
```

The application will start at `http://localhost:7007/` by default.

---

## Move Default Avatar

After running `__init__.py` for the first time, move the default avatar image to the user avatars directory:

```bash
mv default-avatar.jpeg files/user-avatars/
```

This ensures that new users have a default profile picture.

---

## Default Admin User

The `.env` file allows you to configure a default admin user:

| Field      | Example Value                                 |
| ---------- | --------------------------------------------- |
| First Name | Super                                         |
| Last Name  | Administrateur                                |
| Username   | supadist                                      |
| Email      | [admin@example.com](mailto:admin@example.com) |
| Password   | /P@7sw0rd77-+$                                |

> Change these values in `.env` file to secure the admin account.

---

## Dependencies

* Flask
* Flask-JWT-Extended
* Flask-Migrate
* Flask-Mail
* psycopg2-binary
* python-dotenv
* Flasgger (Swagger API docs)

Check `requirements.txt` for the full list of packages.

---

## License

This project is licensed under the MIT License.
