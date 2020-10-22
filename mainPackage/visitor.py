from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import sqlalchemy
from mainPackage.tables import Visitor
from mainPackage import db

visitor = Blueprint("visitor", __name__, static_folder="static", template_folder="templates")

@visitor.route("/")
def visitor_home():
    visitor_username = session["username"]
    return render_template("visitor/v-home-page.html", visitor_username = visitor_username)
