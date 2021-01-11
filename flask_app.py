from flask import render_template, redirect, request, url_for, session
from flask_socketio import emit
from models import app, socketio, User, Messgae
import functools, json


def login_required(function):
    @functools.wraps(function)  # save function name (for url_for('function_name'))
    def secure_function():
        if "username" not in session:
            return redirect(url_for("login"))
        return function()

    return secure_function


@app.route("/chat", methods=["GET"])
@login_required
def chat():
    """Chat webpage, user must be logged in."""
    all_existed_messages = Messgae.dict_list()
    return render_template("chat.html", messages=all_existed_messages, user=session["username"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page, for get return the page, for post if user put the right username
       password redirect to char. Else, return what he did wrong."""
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = request.form
        username, password = form.values() # get password and user from the html form
        user = User.find(username) # the user object

        if user is None: # user does not exists...
            return render_template("login.html", cant_find_user=True, username=username)

        if password != user.password:
            return render_template("login.html", wrong_password=True, username=username)

        session["username"] = username
        return redirect(url_for("chat"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Return register page. If it is get return base page. Else if got user name
        and password render the page, and change it."""

    if request.method == "GET":
        return render_template("register.html")

    else:
        username, password, re_password = request.form.values()
        if User.find(username) is not None: # user already exists
            return render_template("register.html", user_exists=True, username=username)

        else: # user not exists - GOOD
            User.add(username, password) # add the user
            return render_template("register.html", registered=True, username=username)


@app.route("/sendForm", methods=["POST"])
def send_form():
    """Main page form, redirect you to register or to login/"""
    form = request.form
    if "Register" in form: # clicked regiter
        return redirect(url_for("register"))

    elif "Login" in form: # clicked login
        return redirect(url_for("login"))


@app.route("/index")
@app.route("/")
def main():
    """Main page"""
    return render_template("index.html")


@socketio.on("newMessage")
def send_message(data):
    """Event for, when the user send message, we send the message to all users/"""
    # Save the message and get the message object as dictionary
    msg = Messgae.add(session["username"], data["message"]).to_dict() 
    # emit new event for js. The js will add the message to the html.
    emit("recieveMessage", msg, include_self=True, broadcast=True)
    print("Got new message!")


if __name__ == "__main__":
    # it is actuall a json in js when the first line is const url = 
    # the next line are actually json but on js file
    with open(".\\static\\js\\url.js") as file:
        json_file = json.loads(''.join(file.readlines()[1:]))
        ip = json_file["ip"]
        port = json_file["port"]
        url = json_file["url"]
    # print(ip, port, url)
    socketio.run(app)
