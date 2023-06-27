from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

password = ""

def generate_password():
    global password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_password')
def get_password():
    return password

@app.route('/save', methods=['POST'])
def save():
    name = request.form.get('name')
    if name:
        with open('list.json', 'a') as file:
            file.write(name + '\n')
    return jsonify(success=True)

@app.route('/member')
def member():
    data = []
    with open('list.json', 'r') as file:
        data = file.read().splitlines()
    return render_template('member.html', data=data)

@app.route('/secureadmin', methods=['GET', 'POST'])
def secureadmin():
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        if password_attempt == 'your_admin_password':
            with open('list.json', 'w') as file:
                file.write('')
    return render_template('secureadmin.html')

@app.route('/securepasspage')
def securepasspage():
    generate_password()  # Generate new password
    return render_template('securepasspage.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)
