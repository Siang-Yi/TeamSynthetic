from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import sqlalchemy
from mainPackage.tables import Staff
from mainPackage import db

staff = Blueprint("staff", __name__, static_folder="static", template_folder="templates")

@staff.route("/")
def staff_home():
    staff_username = session["username"]
    return render_template("staff/s-home-page.html", staff_username = staff_username)
