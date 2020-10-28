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
from mainPackage.graph import ground_floor_graph, first_floor_graph
app.register_blueprint(loginSignup, url_prefix="/")
app.register_blueprint(visitor, url_prefix="/visitor")
app.register_blueprint(map, url_prefix="/map")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(staff, url_prefix="/staff")

db.create_all()

thread_user_position = Thread()
thread_all_user_position = Thread()
thread_stop_event = Event()

# pointer = 0
# def current_position():
#     global pointer
#     res = path[pointer]
#     if pointer < len(path) - 1:
#         pointer += 1
#     return res

# def set_position():
#     while not thread_stop_event.isSet():
#         coor = current_position()
#         socketio.emit('coordinate', coor, namespace='/test')
#         socketio.sleep(0.1)

def set_all_position():
    while not thread_stop_event.isSet():
        coordinates = Coordinate.query.all()
        coors = []
        all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices
        for vertex in all_vertices:
            vertex.ppl_count = 0
        for coor in coordinates:
            lat = coor.lat
            lng = coor.lng
            coors.append([lat, lng])
            min_dist = inf
            min_vertex = None
            all_vertices = ground_floor_graph.vertices + first_floor_graph.vertices
            for vertex in all_vertices:
                dist = sqrt((vertex.coor[0] - lat)**2 + (vertex.coor[1] - lng) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    min_vertex = vertex
            min_vertex.ppl_count += 1
        ppl_counts = []
        for vertex in all_vertices:
            ppl_counts.append(vertex.ppl_count)
        socketio.emit('all_coordinates', [coors, ppl_counts], namespace='/test')
        socketio.sleep(10)

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread_user_position
    global thread_all_user_position
    # socketio.emit('connect', path, namespace='/test')

    # if not thread_user_position.isAlive():
    #     print("Starting Thread")
    #     thread_user_position = socketio.start_background_task(set_position)

    if not thread_all_user_position.isAlive():
        print("Starting Thread")
        thread_all_user_position = socketio.start_background_task(set_all_position)
