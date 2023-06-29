import os
import random
import json
from string import ascii_letters
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

PASSWORD_FILE = "password.txt"
LIST_FILE = "list.json"
MAX_LIST_SIZE = 35

def generate_password():
    password = ''.join(random.choices(ascii_letters, k=6))
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)

def get_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            password = file.read().strip()
        return password
    else:
        return ""

def update_list(name):
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, "r") as file:
            member_list = json.load(file)
        for i, item in enumerate(member_list):
            if item[1] == "":
                member_list[i] = ("Performer", name)
                break
        else:
            return False
        with open(LIST_FILE, "w") as file:
            json.dump(member_list, file)
        return True
    return False

def get_member_list():
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, "r") as file:
            member_list = json.load(file)
        return member_list
    else:
        return []

def clear_list():
    if os.path.exists(LIST_FILE):
        os.remove(LIST_FILE)

@app.route("/")
def index():
    password = get_password()
    return render_template("index.html", password=password)

@app.route("/get_password")
def get_password_route():
    password = get_password()
    return jsonify(password=password)

@app.route("/securepasspage")
def securepasspage():
    password = get_password()
    return render_template("securepasspage.html", password=password)

@app.route("/member")
def member():
    member_list = get_member_list()
    return render_template("member.html", member_list=member_list)

@app.route("/secureadmin")
def secureadmin():
    member_list = get_member_list()
    return render_template("secureadmin.html", member_list=member_list)

@app.route("/update", methods=["POST"])
def update():
    password = request.form.get("password")
    name = request.form.get("name")
    if password and password.lower() == get_password().lower():
        if name:
            if update_list(name):
                return redirect(url_for("member"))
            else:
                return "Sorry, there are no more available slots tonight."
    return redirect(url_for("index"))

@app.route("/randomize", methods=["POST"])
def randomize():
    member_list = get_member_list()
    random.shuffle(member_list)
    with open(LIST_FILE, "w") as file:
        json.dump(member_list, file)
    return redirect(url_for("secureadmin"))

@app.route("/clear", methods=["POST"])
def clear():
    clear_list()
    return redirect(url_for("secureadmin"))

if __name__ == "__main__":
    generate_password()
    app.run(debug=True)
