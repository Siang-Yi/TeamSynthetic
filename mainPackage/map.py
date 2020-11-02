from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session, jsonify
from flask_sqlalchemy import sqlalchemy
from mainPackage import db
from mainPackage.graph import ground_floor_graph, first_floor_graph
import time

map = Blueprint("map", __name__, static_folder="static", template_folder="templates")

@map.route("/", methods=["POST", "GET"])
def home(ground_floor = [True], nodes=[[], []]):
    if request.method == "GET":
        if ground_floor[0]:
            graph = ground_floor_graph
        else:
            graph = first_floor_graph

        all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices

        points = []  
        ppl_counts = []
        for vertex in all_vertices:
            points.append(vertex.coor)
            ppl_counts.append(vertex.ppl_count)

        location_names = graph.get_location_names()
        return render_template("map/map.html", points = points, ppl_counts=ppl_counts, nodes_coor = [], location_names = location_names, ground_floor=ground_floor[0])

    if request.method == "POST":
        all_graph = [ground_floor_graph, first_floor_graph]
        if ground_floor[0]:
            graph = ground_floor_graph
            current_floor = 0
        else:
            graph = first_floor_graph
            current_floor = 1
        all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices
        points = []
        ppl_counts = []
        for vertex in all_vertices:
            points.append(vertex.coor)
            ppl_counts.append(vertex.ppl_count)
        location_names = graph.get_location_names()
        form = request.form
        if "search" in form:
            print(request.form["search"])
        elif "location" in form:
            key = request.form["location"]
            vertex, same, link = graph.get_vertex(key, ground_floor[0])
            if current_floor == 0:
                next_floor = 1
            else:
                next_floor = 0
            current = graph.user_nearest_node()  # current loc
            if same:
                nodes[current_floor] = graph.path(current, vertex)
                nodes[next_floor] = []
            else:
                next_floor_graph = all_graph[next_floor]
                link_vertex, connect_link = graph.shortest_link(current, link, next_floor_graph, vertex)
                nodes[current_floor] = all_graph[current_floor].path(current, link_vertex)
                nodes[next_floor] = all_graph[next_floor].path(connect_link, vertex)

            nodes_coor = []
            for i in range(len(nodes)):
                nodes_per_floor = []
                for j in range(len(nodes[i])):
                    nodes_per_floor.append(all_graph[i].vertices[nodes[i][j]].coor)
                nodes_coor.append(nodes_per_floor)
            return render_template("map/map.html", points = points, ppl_counts=ppl_counts, nodes_coor = nodes_coor, location_names = location_names, ground_floor=ground_floor[0])
        else:
            if ground_floor[0]:
                ground_floor[0] = False
                graph = first_floor_graph
            else:
                ground_floor[0] = True
                graph = ground_floor_graph

            all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices
            points = []
            for vertex in all_vertices:
                points.append(vertex.coor)
            
            nodes_coor = []
            for i in range(len(nodes)):
                nodes_per_floor = []
                for j in range(len(nodes[i])):
                    nodes_per_floor.append(all_graph[i].vertices[nodes[i][j]].coor)
                nodes_coor.append(nodes_per_floor)

            return render_template("map/map.html", points = points, ppl_counts=ppl_counts, nodes_coor = nodes_coor, location_names = location_names, ground_floor=ground_floor[0])
