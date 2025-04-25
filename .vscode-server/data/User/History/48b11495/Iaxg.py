import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'your-secret-key-here'
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') or 'localhost'
app.config['MYSQL_USER