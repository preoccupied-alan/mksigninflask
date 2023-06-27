from flask import Flask, render_template, request, jsonify
import random
import string
import json
import time

app = Flask(__name__)

password_file = "password.txt"
list_file = "list.json"
admin_password = "admin123"  # Change this to your desired administrator password


def generate_password():
    while True:
        password = ''.join(random.choices(string.ascii_uppercase, k=6))
        with open(password_file, "w") as file:
            file.write(password)
        time.sleep(60)  # Wait for 60 seconds before generating the next password


def update_list(name):
    with open(list_file, "r") as file:
        data = json.load(file)
    for slot in range(1, 41):
        if f"Slot {slot}" not in data:
            data[f"Slot {slot}"] = name
            break
    with open(list_file, "w") as file:
        json.dump(data, file)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    password = request.form.get("password")
    name = request.form.get("name")
    if password.lower() == open(password_file).read().strip().lower():
        update_list(name)
        return render_template("member.html")
    else:
        return render_template("index.html", error="Invalid password. Please try again.")


@app.route("/get_password")
def get_password():
    with open(password_file, "r") as file:
        password = file.read().strip()
    return jsonify(password=password)


@app.route("/admin")
def admin():
    password = request.args.get("password")
    if password == admin_password:
        with open(list_file, "r") as file:
            data = json.load(file)
        return render_template("secureadmin.html", data=data)
    else:
        return render_template("secureadmin.html", error="Invalid password. Please try again.")


@app.route("/randomize")
def randomize():
    password = request.args.get("password")
    if password == admin_password:
        with open(list_file, "r") as file:
            data = json.load(file)
        slots = list(data.keys())
        random.shuffle(slots)
        data = {slot: data[slot] for slot in slots}
        with open(list_file, "w") as file:
            json.dump(data, file)
    return render_template("secureadmin.html")


@app.route("/reset")
def reset():
    password = request.args.get("password")
    if password == admin_password:
        data = {f"Slot {slot}": "" for slot in range(1, 41)}
        with open(list_file, "w") as file:
            json.dump(data, file)
    return render_template("secureadmin.html")


@app.route("/securepasspage")
def securepasspage():
    password = request.args.get("password")
    if password == admin_password:
        with open(password_file, "r") as file:
            password = file.read().strip()
        return render_template("securepasspage.html", password=password)
    else:
        return render_template("securepasspage.html", error="Invalid password. Please try again.")


if __name__ == "__main__":
    generate_password()  # Generate initial password on server startup
    app.run(debug=True)
