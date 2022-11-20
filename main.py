from flask import Flask, render_template, request, redirect, url_for
from replit import db,web

app = Flask(__name__)

user = web.UserStore()


@app.route('/')
def index():
    if web.auth.name != "":
        return redirect("/home")
    return render_template('login.html')

@app.route('/home')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def home():
    if web.auth.name not in db["users"]:
        db["users"].append(web.auth.name)
    return render_template('home.html')

@app.route('/new')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def new():
    return render_template('new.html')

@app.route('/new/question')
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def question():
    return render_template('question.html')

@app.route("/set")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def set():
    return render_template('set.html')

@app.route("/right")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def correct():
    return render_template('correct.html')

@app.route("/wrong")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def wrong():
    return render_template('wrong.html')

app.run(host='0.0.0.0', port=80,debug=True)