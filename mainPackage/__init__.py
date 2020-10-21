from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
import pymysql
from time import sleep
from random import random
from threading import Thread, Event

app = Flask(__name__)
app.secret_key = "hello"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12368780:cYKqlW55kh@sql12.freemysqlhosting.net/sql12368780' later change to this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

from mainPackage.map import map
app.register_blueprint(map, url_prefix="/")

db.create_all()

thread = Thread()
thread_stop_event = Event()

path =[]
def custom_path():
    global path
    x = 0.05
    y = 0.04
    for i in range(10):
        path.append([x, y])
        y += 0.02

    for i in range(5):
        path.append([x, y])
        x += 0.02

    for i in range(10):
        path.append([x, y])
        y -= 0.02

    for i in range(15):
        path.append([x, y])
        x += 0.02

    for i in range(11):
        path.append([x, y])
        y += 0.02

custom_path()

pointer = 0
def current_position():
    global pointer
    res = path[pointer]
    if pointer < len(path) - 1:
        pointer += 1
    return res

def set_position():
    while not thread_stop_event.isSet():
        coor = current_position()
        socketio.emit('coordinate', coor, namespace='/test')
        socketio.sleep(0.1)

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    global path
    print(path)
    socketio.emit('connect', path, namespace='/test')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(set_position)