from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.secret_key = "hello"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12368780:cYKqlW55kh@sql12.freemysqlhosting.net/sql12368780' later change to this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# from teamHd.admin import admin
# from teamHd.teacher import teacher
# from teamHd.student import student
# from teamHd.loginSignup import loginSignup
# app.register_blueprint(loginSignup, url_prefix="/")
# app.register_blueprint(admin, url_prefix="/admin")
# app.register_blueprint(teacher, url_prefix="/teacher")
# app.register_blueprint(student, url_prefix="/student")

db.create_all()
