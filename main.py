import functions as fun
from flask import Flask, render_template, request, redirect
from replit import db,web
import random
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
        user.current["sets"] = {}
        user.current["id"] = 0
        user.current["current"] = []
    if len(user.current["sets"]) > 0:
        sets = fun.make_dict(user.current["sets"])
    else:
        sets = {}
    return render_template('home.html',sets=sets)

@app.route('/new',methods=["POST","GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def new():
    if request.method == "POST":
        user.current["id"] += 1
        id = user.current["id"]
        title = request.form["title"]
        desc = request.form["desc"]
        background = "static/backgrounds/"+request.form["background"]+".png"
        user.current["sets"][id] = {"setup":{"title":title.title(), "desc":desc, "background":background},}
        return redirect("/new/question")
    return render_template('new.html')

@app.route('/new/question',methods=["POST","GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def question():
    if request.method == "POST":
        title = request.form["title"]
        ans = request.form["ans"]
        sets = user.current["sets"]
        sets[str(user.current["id"])]["Q"+str(len(sets[str(user.current["id"])]))] = {"title":title, "ans":ans}
        user.current["sets"] = sets
        if request.form['button'] == "finsh":
            return redirect("/home")
    return render_template('question.html')

@app.route("/set")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def set():
    return render_template('set.html')

@app.route("/set/<id>",methods=["POST","GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def do_set(id):
    order = list(user.current["current"])
    if request.method == "POST":
        try:
            request.form["button"]
        except:
            order[0] += 1
            user.current["current"] = order
            if order[0] == len(order):
                return render_template("done.html")

        else:
            try:
                request.form["text"]
            except:
                what_ans = request.form["button"]
            else:
                what_ans = request.form["text"]
            sets = fun.make_dict(user.current["sets"])
            quest = str(order[order[0]])
            ans = sets[id]["Q"+quest]["ans"]
            question = sets[id]["Q"+quest]["title"]
            if ans == what_ans:
                return render_template('correct.html',question=question, ans=ans)
            else:
                if random.randint(0,1) == 0:
                    user.current["current"].append(order[order[0]])
                return render_template('wrong.html',question=question, ans=ans) 
    else:
        set = fun.make_dict(user.current["sets"])[id]
        set_len = len(set) - 1
        order = []
        while True:
            ran = random.randint(1,set_len)
            if ran not in order:
                order.append(ran)
            if len(order) == set_len:
                order.insert(0,1)
                break
        user.current["current"] = order
    order = list(user.current["current"])
    if len(fun.make_dict(user.current["sets"])[id])-1 < 3:
        question = fun.make_dict(user.current["sets"])[id]["Q"+str(order[order[0]])]["title"]
        return render_template('set2.html',question=question)
    else:
        set_len = len(order)-1
        ran1 = random.randint(1,set_len)
        ran2 = random.randint(1,set_len)
        while ran1 == ran2 or order[ran1] == order[order[0]] or order[ran2] == order[order[0]] or order[ran1] == order[ran2]:
            ran1 = random.randint(1,set_len)
            ran2 = random.randint(1,set_len)
        print(order[order[0]])
        print(order[ran1])
        print(order[ran2])
        set = fun.make_dict(user.current["sets"])[id]
        question = set["Q"+str(order[order[0]])]["title"]
        ans = [set["Q"+str(order[order[0]])]["ans"],set["Q"+str(order[ran1])]["ans"],set["Q"+str(order[ran2])]["ans"]]
        ran1 = random.randint(0,len(ans)-1);ans1 = ans[ran1];ans.pop(ran1)
        ran2 = random.randint(0,len(ans)-1);ans2 = ans[ran2];ans.pop(ran2)
        ans3 = ans[0]
        return render_template('set.html',question=question, ans1=ans1,ans2=ans2,ans3=ans3)

@app.route("/set/del/<id>")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def del_set(id):
    sets = fun.make_dict(user.current["sets"])
    del sets[id]
    user.current["sets"] = sets
    return redirect("/home")


@app.route("/set2")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def done():
    return render_template('set2.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

@app.route("/veiw")
def veiw():
    return fun.make_dict(user.current["sets"])
app.run(host='0.0.0.0', port=80,debug=True)