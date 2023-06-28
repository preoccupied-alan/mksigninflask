from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Define the maximum list size
max_list_size = 35

# Load the initial member list from list.json
with open('list.json', 'r') as file:
    member_list = json.load(file)

@app.route('/')
def index():
    return render_template('index.html', member_list=member_list, max_list_size=max_list_size)

@app.route('/save', methods=['POST'])
def save():
    name = request.form.get('name')
    if name:
        if len(member_list) < max_list_size:
            member_list.append(name)
            with open('list.json', 'w') as file:
                json.dump(member_list, file)
            return redirect(url_for('member'))
        else:
            message = 'The list is full. Cannot add more members.'
    else:
        message = 'Name field cannot be empty.'

    return render_template('index.html', member_list=member_list, max_list_size=max_list_size, message=message)

@app.route('/member')
def member():
    return render_template('member.html', member_list=member_list)

@app.route('/securepasspage')
def securepasspage():
    return render_template('securepasspage.html')

@app.route('/get_password')
def get_password():
    with open('password.txt', 'r') as file:
        password = file.read()
    return password

if __name__ == '__main__':
    app.run()
