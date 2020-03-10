from flask import Flask,json,request
import requests

app = Flask(__name__)

@app.route("/")
def write_to_screen():
    username = get_username()
    eInName = if_user_has_E_in_name(username)
    length = check_length_of_user(username)

    

def get_username():
    username = request.args.get("username")
    return username

def if_user_has_E_in_name(username):
    if "E","e" in username:
        return "De gebruiker heeft een e in zijn/haar gebruikersnaam."

def check_length_of_user(username):
    if len(username) > 10:
        return "Dit is een lange gebruikersnaam namelijk ", len(username), " tekens."