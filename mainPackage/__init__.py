from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
import pymysql
from time import sleep
from random import random
from threading import Thread, Event
from math import inf, sqrt

app = Flask(__name__)
app.secret_key = "hello"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12368780:cYKqlW55kh@sql12.freemysqlhosting.net/sql12368780' later change to this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

from mainPackage.map import map
from mainPackage.loginSignup import loginSignup
from mainPackage.visitor import visitor
from mainPackage.admin import admin
from mainPackage.staff import staff
from mainPackage.tables import *
from mainPackage.graph import *
app.register_blueprint(loginSignup, url_prefix="/")
app.register_blueprint(visitor, url_prefix="/visitor")
app.register_blueprint(map, url_prefix="/map")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(staff, url_prefix="/staff")

db.create_all()

thread_user_position = Thread()
thread_all_user_position = Thread()
thread_stop_event = Event()


def set_position():
    while not thread_stop_event.isSet():
        user = Visitor.query.filter(Visitor.username=="user").first()
        print("run")
        user_coor = user.coordinate[0]
        lng = user_coor.lng
        lat = user_coor.lat
        if 0 <= lng <= 2.25 and 0 <= lat <= 1.1:  # ground floor
            ground_floor_graph.user_coor = [lng, lat]
            first_floor_graph.user_coor = None
        else:
            first_floor_graph.user_coor = [lng, lat]
            ground_floor_graph.user_coor = None

        socketio.emit('coordinate', [lng, lat], namespace='/test')
        print(lng, lat)
        socketio.sleep(3)

def set_all_position():
    while not thread_stop_event.isSet():
        ground_floor_graph.add_edges(groud_floor_edges)
        first_floor_graph.add_edges(first_floor_edges)
        user = Visitor.query.filter(Visitor.username=="user").first()
        user_id = user.id
        coordinates = Coordinate.query.filter(Coordinate.visitor_id != user_id).all()
        coors = []
        all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices
        for vertex in all_vertices:
            vertex.ppl_count = 0
        for coor in coordinates:
            lat = coor.lat
            lng = coor.lng
            coors.append([lng, lat])
            min_dist = inf
            min_vertex = None
            all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices

            in_room = False
            for key, item in all_floor_locations_area[0].items():
                top_left = item[0]
                bottom_right = item[1]
                if lat < top_left[0] and lat > bottom_right[0] and lng > top_left[1] and lng < bottom_right[1]:
                    vertex_number = ground_floor_graph.locations[0][key]
                    min_vertex = ground_floor_graph.vertices[vertex_number]
                    in_room = True
                    break

            if in_room == False:
                for key, item in all_floor_locations_area[1].items():
                    top_left = item[0]
                    bottom_right = item[1]
                    if lat < top_left[0] and lat > bottom_right[0] and lng > top_left[1] and lng < bottom_right[1]:
                        vertex_number = first_floor_graph.locations[1][key]
                        min_vertex = first_floor_graph.vertices[vertex_number]
                        in_room = True
                        break
                        
            if not in_room:
                for vertex in all_vertices:
                    if vertex.in_room == False:
                        dist = sqrt((vertex.coor[1] - lat)**2 + (vertex.coor[0] - lng) ** 2)
                        if dist < min_dist:
                            min_dist = dist
                            min_vertex = vertex

            min_vertex.ppl_count += 1
            vertex_id = min_vertex.id
            vertex_graph = min_vertex.floor
            if vertex_graph == 0:
                ground_floor_graph.add_people(vertex_id)
            else:
                first_floor_graph.add_people(vertex_id)

        ground_floor_graph.floyd_warshall()
        first_floor_graph.floyd_warshall()

        ppl_counts = []
        for vertex in all_vertices:
            ppl_counts.append(vertex.ppl_count)

        area_arr = []
        for pair in all_floor_locations_area[0].values():
                for coor in pair:
                    area_arr.append([coor[1], coor[0]])

        for pair in all_floor_locations_area[1].values():
            for coor in pair:
                area_arr.append([coor[1], coor[0]])

        socketio.emit('all_coordinates', [coors, ppl_counts], namespace='/test')
        socketio.sleep(6)

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread_user_position
    global thread_all_user_position
    # socketio.emit('connect', path, namespace='/test')

    if not thread_user_position.isAlive():
        print("Starting Thread User Pos")
        thread_user_position = socketio.start_background_task(set_position)

    if not thread_all_user_position.isAlive():
        print("Starting Thread All Pos")
        thread_all_user_position = socketio.start_background_task(set_all_position)
