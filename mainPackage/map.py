from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session, jsonify
from flask_sqlalchemy import sqlalchemy
from mainPackage import db
from mainPackage.graph import ground_floor_graph
import time

map = Blueprint("map", __name__, static_folder="static", template_folder="templates")

@map.route("/", methods=["POST", "GET"])
def home(ground_floor = [True]):
    if request.method == "POST":
        vertices = ground_floor_graph.vertices
        points = []
        for vertex in vertices:
            points.append(vertex.coor)
        location_names = ground_floor_graph.get_location_names()
        form = request.form
        if "search" in form:
            print(request.form["search"])
        elif "location" in form:
            key = request.form["location"]
            vertex = ground_floor_graph.get_vertex(key)
            nodes = ground_floor_graph.path(0, vertex)
            nodes_coor = []
            for node in nodes:
                nodes_coor.append(ground_floor_graph.vertices[node].coor)
            return render_template("map/map.html", points = points, nodes_coor = nodes_coor, location_names = location_names, ground_floor=ground_floor[0])
        else:
            print(ground_floor[0])
            if ground_floor[0]:
                ground_floor[0] = False
            else:
                ground_floor[0] = True
            print(ground_floor[0])
            return render_template("map/map.html", points = points, nodes_coor = [], location_names = location_names, ground_floor=ground_floor[0])

    vertices = ground_floor_graph.vertices
    points = []
    for vertex in vertices:
        points.append(vertex.coor)
    
    location_names = ground_floor_graph.get_location_names()
    return render_template("map/map.html", points = points, nodes_coor = [], location_names = location_names, ground_floor=ground_floor[0])
