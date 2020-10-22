from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session, jsonify
from flask_sqlalchemy import sqlalchemy
from mainPackage import db
from mainPackage.graph import ground_floor_graph
import time

map = Blueprint("map", __name__, static_folder="static", template_folder="templates")

@map.route("/", methods=["POST", "GET"])
def home():
    vertices = ground_floor_graph.vertices
    points = []
    for vertex in vertices:
        points.append(vertex.coor)
    nodes = ground_floor_graph.path(0, 18)
    nodes_coor = []
    for node in nodes:
        nodes_coor.append(ground_floor_graph.vertices[node].coor)
    print(nodes_coor)
    return render_template("map/map.html", points = points, nodes_coor = nodes_coor)
