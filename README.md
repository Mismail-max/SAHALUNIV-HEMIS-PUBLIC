# 📚  SahalUniv-Hemis

This is a Flask-based web application that allows users to search for student records by ID and allows administrators to upload student data via CSV. The app is containerized using Docker and managed with Docker Compose.

---

## 🚀 Features

-  Search for student information by University ID
-  Upload CSV file (Admin only)
-  MySQL backend for storing student records
-  Dockerized for easy deployment
-  Responsive UI with Bootstra
---

## 🧰 Requirements
- python -m venv venv
- source venv/bin/activate  # On Windows use: venv\Scripts\activate
- pip install -r requirements.txt

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 📦 How to Run (with Docker Compose)

1. **Clone this repository:**

   ```bash
   git clone https://github.com/Mismail-max/SAHALUNIV-HEMIS-PUBLIC.git
   cd SAHALUNIV-HEMIS-PUBLIC
   ```
2. **Create a local .env file with the below content**  
   ```
   MYSQL_ROOT_PASSWORD=<set>
   DB_HOST=localhost
   DB_PASSWORD=<set>
   DB_USER=<set>
   DB_NAME=hemis
   DB_PORT=3306
   SECRET_KEY=<set>
   ```
3. **Run the app and test it**

   ```
   docker-compose up --build
   ```
  -  Visit: http://localhost:5001
  - Upload the sample data in /uploads folder
---

# 🔧 Contributing
## 🚨 IMPORTANT: Please do not commit directly to main.

If you're contributing:

1. Create a new branch from main:
    ```
    git checkout -b your-feature-name
    ```
2. Make your changes.

3. Commit and push to your branch:
    ```
    git push origin your-feature-name
    ```
4. Open a Pull Request and describe your changes clearly.

## 🌐 URL Endpoints

- `/` – Home page with student search and record view  
- `/` – Upload CSV (visible only when logged in)  
- `/login` – User login form  
- `/register` – New user registration  
- `/logout` – Log out the current user  
- `/update_creds` – Change password (logged-in users only)  
