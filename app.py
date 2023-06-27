from flask import Flask, render_template, request, jsonify
import random
import json

app = Flask(__name__)

password = ""

def generate_password():
    global password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html', password=password)

@app.route('/get_password')
def get_password():
    return password

@app.route('/save', methods=['POST'])
def save():
    name = request.form.get('name')
    if name:
        with open('list.json', 'r+') as file:
            data = json.load(file)
            available_index = None
            for i in range(len(data)):
                if data[i] is None:
                    available_index = i
                    break
            if available_index is not None:
                data[available_index] = name
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="List is full")

    return jsonify(success=False, message="Invalid request")

@app.route('/member')
def member():
    with open('list.json', 'r') as file:
        data = json.load(file)
    return render_template('member.html', data=data)

@app.route('/secureadmin', methods=['GET', 'POST'])
def secureadmin():
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        if password_attempt == 'your_admin_password':
            with open('list.json', 'w') as file:
                json.dump([None] * 10, file)
    return render_template('secureadmin.html')

@app.route('/securepasspage')
def securepasspage():
    return render_template('securepasspage.html', password=password)

if __name__ == '__main__':
    generate_password()  # Generate initial password
    app.run(debug=True)
