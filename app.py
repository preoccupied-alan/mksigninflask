import os
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

PASSWORD_FILE = "password.txt"
LIST_FILE = "list.json"
MAX_LIST_SIZE = 35

def check_password(password):
    with open(PASSWORD_FILE, "r") as file:
        stored_password = file.read().strip()
    return password == stored_password

def get_member_list():
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, "r") as file:
            member_list = json.load(file)
        return member_list
    else:
        return []

def save_member_list(member_list):
    with open(LIST_FILE, "w") as file:
        json.dump(member_list, file)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    member_list = get_member_list()

    if request.method == "POST":
        password = request.form.get("password")
        if check_password(password):
            if len(member_list) < MAX_LIST_SIZE:
                name = request.form.get("name")
                if name:
                    if name in member_list:
                        message = "Name already exists in the list."
                    else:
                        member_list.append(name)
                        save_member_list(member_list)
                        return redirect(url_for("member"))
                else:
                    message = "Name field is empty."
            else:
                message = "The list is full. Cannot add more members."
        else:
            message = "Incorrect password. Please try again."

    return render_template("index.html", message=message, member_list=member_list, max_list_size=MAX_LIST_SIZE)


@app.route("/member")
def member():
    member_list = get_member_list()
    return render_template("member.html", member_list=member_list)


if __name__ == "__main__":
    app.run(debug=True)
