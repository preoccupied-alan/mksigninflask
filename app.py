from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

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
    with open('password.txt', 'r') as file:
        password = file.read()
    return render_template('securepasspage.html', password=password)

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
    app.run(debug=True)
