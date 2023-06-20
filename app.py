from flask import Flask, render_template, request, redirect, jsonify
import json
import string
import random
import threading

app = Flask(__name__)

# Global variables
password = ""
name_input_enabled = False
submit_button_enabled = False

def generate_password():
    global password
    password = ''.join(random.choices(string.ascii_uppercase, k=6))
    threading.Timer(60, generate_password).start()

def update_credentials():
    threading.Timer(30, update_credentials).start()
    with open('password.txt', 'w') as file:
        file.write(password)

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
    return render_template('securepasspage.html', password=password)

@app.route('/get_password')
def get_password():
    return jsonify({'password': password})

@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    with open('list.json', 'r') as file:
        data = json.load(file)
    available_slot = next((slot for slot, value in data.items() if not value), None)
    if available_slot:
        data[available_slot] = name
        with open('list.json', 'w') as file:
            json.dump(data, file)
        return redirect('/member')
    else:
        return 'No available slots for saving the name.'

if __name__ == '__main__':
    generate_password()
    update_credentials()
    app.run(debug=True)
