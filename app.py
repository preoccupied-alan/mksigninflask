from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

password = ""
data = []

def generate_password():
    global password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_password')
def get_password():
    if not password:
        generate_password()
    return password

@app.route('/check_password', methods=['POST'])
def check_password():
    user_password = request.form.get('password')
    if user_password == password:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/save', methods=['POST'])
def save():
    name = request.form.get('name')
    if name:
        data.append(name)  # Append the name to the in-memory data list
        with open('list.json', 'a') as file:
            file.write(name + '\n')
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/member')
def member():
    return render_template('member.html', data=data)

@app.route('/secureadmin', methods=['GET', 'POST'])
def secureadmin():
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        if password_attempt == 'your_admin_password':
            data.clear()  # Clear the in-memory data list
            with open('list.json', 'w') as file:
                file.write('')
    return render_template('secureadmin.html')

if __name__ == '__main__':
    generate_password()  # Generate initial password
    app.run(debug=True)
