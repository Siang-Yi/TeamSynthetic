from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import sqlalchemy
from mainPackage.tables import Visitor, Staff
from mainPackage import db

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route("/")
def admin_home():
    return render_template("admin/a-home-page.html")

@admin.route("/a-create-staff-acc", methods=["POST", "GET"])
def admin_create_acc():
    if request.method =="POST":
        email = request.form["email"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        job = request.form["job"]
        username = request.form["username"]
        password = request.form["password"]

        invalidInput = False
        found_username = Staff.query.filter(Staff.username == username).first()
        found_email = Staff.query.filter(Staff.email == email).first()
        if found_email:
            flash("This email has alread been registered")
            invalidInput = True
        elif not 0 < len(firstName) <= 20:
            flash("Invalid first name")
            invalidInput = True
        elif not 0 < len(lastName) <= 20:
            flash("Invalid last name")
            invalidInput = True
        elif not 0 < len(username) <= 50:
            flash("Invalid username")
            invalidInput = True
        elif not 0 < len(job) <= 15:
            flash("Invalid job title")
            invalidInput = True
        elif found_username:
            flash("This username is unavailable")
            invalidInput = True
        elif not 0 < len(password) <= 20:
            flash("Invalid password")
            invalidInput = True
        if invalidInput:
            return render_template("admin/a-create-staff-acc.html", emailText = email, firstNameText = firstName, lastNameText = lastName, jobText = job, usernameText = username)


        staff = Staff(email, firstName, lastName, job, username, password)
        try:
            db.session.add(staff)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
        #return render_template("login.html")
    return render_template("admin/a-create-staff-acc.html")
