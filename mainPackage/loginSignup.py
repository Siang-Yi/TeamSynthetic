from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session
from mainPackage.tables import Visitor, Staff
from mainPackage import db
import os
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import and_

loginSignup = Blueprint("loginSignup", __name__, static_folder="static", template_folder="templates")

@loginSignup.route("/", methods=["POST", "GET"])
def home():
    if request.method =="POST":
        role = request.form["role"]
        username = request.form["username"]
        password = request.form["password"]
        session["role"] = role
        session["username"] = username
        if role == "visitor":
            foundVisitor = Visitor.query.filter(and_(Visitor.username == username,Visitor.password == password)).first()
            if foundVisitor:
                return redirect(url_for("visitor.visitor_home"))
            else:
                flash("Username or password is wrong", "info")

        elif role == "staff":
            foundStaff = Staff.query.filter(and_(Staff.username == username, Staff.password == password)).first()
            if foundStaff:
                return redirect(url_for("staff.staff_home"))
            else:
                flash("Username or password is wrong","info")

        elif role == "select":
            flash("Please choose a role to login as","info")

        elif role == "admin" and username == "admin" and password == "admin":
            return redirect(url_for("admin.admin_home"))
        else:
            flash("Username or password is wrong", "info")

    return render_template("login.html")

@loginSignup.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method =="POST":
        email = request.form["email"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        username = request.form["username"]
        password = request.form["password"]

        invalidInput = False
        found_username = Visitor.query.filter(Visitor.username == username).first()
        found_email = Visitor.query.filter(Visitor.email == email).first()
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
        elif found_username:
            flash("This username is unavailable")
            invalidInput = True
        elif not 0 < len(password) <= 20:
            flash("Invalid password")
            invalidInput = True
        if invalidInput:
            return render_template("signup.html", emailText = email, firstNameText = firstName, lastNameText = lastName, usernameText = username)

        visitor = Visitor(email, firstName, lastName, username, password)
        try:
            db.session.add(visitor)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
        return redirect(url_for("loginSignup.home"))
    return render_template("signup.html")
