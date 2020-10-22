from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import sqlalchemy
from mainPackage.tables import Visitor, Staff
from mainPackage import db

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route("/")
def admin_home():
    return render_template("admin/a-home-page.html")
