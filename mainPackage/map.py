from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session, jsonify
from flask_sqlalchemy import sqlalchemy
from mainPackage import db
import time

map = Blueprint("map", __name__, static_folder="static", template_folder="templates")

@map.route("/", methods=["POST", "GET"])
def home():
    return render_template("map/map.html")
