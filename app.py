from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

PASSWORD_FILE = 'password.txt'
password = ""

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

@app.route('/')
def index():
    read_password()
    return render_template('index.html', password=password)

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

# Rest of the code remains the same

if __name__ == '__main__':
    generate_password()  # Generate initial password
    app.run(debug=True)
