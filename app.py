from controllers.student_controller import student_routes
from controllers.auth_controller import auth_routes
from flask import Flask
import pandas as pd
import mysql.connector
import os
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(student_routes)
app.register_blueprint(auth_routes) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)