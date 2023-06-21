from flask import Flask, render_template, request, redirect, jsonify
import json
import string
import random
import threading
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Global variables
password = ""

def generate_password():
    global password
    password = ''.join(random.choices(string.ascii_uppercase, k=6))
    threading.Timer(60, generate_password).start()
    emit_password_update(password)  # Send real-time password update

def emit_password_update(password):
    socketio.emit('password_update', {'password': password}, namespace='/realtime')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    with open('list.json', 'r') as file:
        data = json.load(file)
    return render_template('member.html', data=data)

@app.route('/secureadmin')
def secureadmin():
    with open('list.json', 'r') as file:
        data = json.load(file)
    return render_template('secureadmin.html', data=data)

@app.route('/securepasspage')
def securepasspage():
    return render_template('securepasspage.html')

@app.route('/get_password')
def get_password():
    return jsonify({'password': password})

@app.route('/save', methods=['POST'])
def save():
    # Existing save logic goes here
    pass

@socketio.on('connect', namespace='/realtime')
def on_connect():
    emit_password_update(password)  # Send initial password when WebSocket connects

if __name__ == '__main__':
    generate_password()
    socketio.run(app, debug=True)
