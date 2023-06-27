from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

PASSWORD_FILE = 'password.txt'
LIST_FILE = 'list.json'
MAX_LIST_SIZE = 10

password = ""
member_list = []

def generate_password():
    global password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.choice(characters) for _ in range(6))
    with open(PASSWORD_FILE, 'w') as file:
        file.write(password)

def read_password():
    global password
    with open(PASSWORD_FILE, 'r') as file:
        password = file.read().strip()

def read_member_list():
    global member_list
    with open(LIST_FILE, 'r') as file:
        member_list = file.read().splitlines()

def write_member_list():
    with open(LIST_FILE, 'w') as file:
        file.write('\n'.join(member_list))

@app.route('/')
def index():
    read_password()
    return render_template('index.html', password=password, member_list=member_list)

@app.route('/get_password')
def get_password():
    read_password()
    return password

@app.route('/update_password', methods=['POST'])
def update_password():
    global password
    new_password = request.form.get('new_password')
    if new_password:
        password = new_password.strip()
        with open(PASSWORD_FILE, 'w') as file:
            file.write(password)
        return jsonify(success=True, message="Password updated successfully")

    return jsonify(success=False, message="Invalid request")

@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form.get('name')
    if name:
        if len(member_list) >= MAX_LIST_SIZE:
            return jsonify(success=False, message="List is full")

        member_list.append(name.strip())
        write_member_list()
        return jsonify(success=True, message="Member added successfully")

    return jsonify(success=False, message="Invalid request")

@app.route('/member')
def member():
    read_member_list()
    return render_template('member.html', member_list=member_list)

@app.route('/secureadmin', methods=['GET', 'POST'])
def secureadmin():
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        if password_attempt == password:
            member_list.clear()
            write_member_list()
    return render_template('secureadmin.html')

@app.route('/securepasspage')
def securepasspage():
    read_password()
    return render_template('securepasspage.html', password=password)

if __name__ == '__main__':
    generate_password()  # Generate initial password
    app.run(debug=True)
