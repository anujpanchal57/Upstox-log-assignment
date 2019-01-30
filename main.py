from pprint import pprint
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from flask_socketio import SocketIO, join_room, leave_room, emit, send
import os
from time import time
import shortuuid

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('join')
def join_connection(data):
    logs = []
    filename = "logger/logger.txt"
    file = open(filename, "r")
    for line in file:
        logs.append(line)
    emit('logger', {'logs': logs[-10:]})

@socketio.on('logger_update')
def logger_update(data):
    logs = []
    filename = "logger/logger.txt"
    with open(filename, "a") as log_file:
        log_file.write("New log added --> " + str(shortuuid.uuid()) + str(shortuuid.uuid()) + '\n')
    file = open(filename, "r")
    for line in file:
        logs.append(line)
    emit('logger', {'logs': logs[-10:]})
    


if __name__ == '__main__':
    socketio.run(host='0.0.0.0', port=5000, app=app)