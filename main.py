import functions as fun
from flask import Flask, render_template, request, redirect
from replit import db,web
import random, sys
from better_profanity import profanity

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
    return render_template('home.html',sets=sets,profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

@app.route('/new',methods=["POST","GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def new():
    if int(sys.getsizeof(fun.make_dict(user.current["sets"]))) >= 4900:
        return render_template("error.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name ,error_title="You have ran out of storage.",error="You have reach the max amount of storage that you have please deleat a set to make a new one.",link="/home")
    if request.method == "POST":
        user.current["id"] += 1
        id = user.current["id"]
        title = profanity.censor(request.form["title"])
        desc = profanity.censor(request.form["desc"])
        if len(title) == 0 or len(desc) == 0 or len(desc) > 500 or len(title) > 100:
            return render_template("error.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name,error_title="Too Long Or Short",error="The title or desciption is to long or to short please go back and make a new one.",link="/new")
        background = "static/backgrounds/"+request.form["background"]+".png"
        user.current["sets"][id] = {"setup":{"title":title.title(), "desc":desc, "background":background,"user":web.auth.name},}
        return redirect("/new/question")
    return render_template('new.html',profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

@app.route('/new/question',methods=["POST","GET"])
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def question():
    if request.method == "POST":
        title = profanity.censor(request.form["title"])
        ans = profanity.censor(request.form["ans"])
        sets = fun.make_dict(user.current["sets"])
        if len(title) == 0 or len(ans) == 0 or len(ans) > 200 or len(title) > 100:
            return render_template("error.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name ,error_title="Too Long Or Short",error="The question or answer is to long or to short please go back and make a new one.",link="/new/question")
        sets[str(user.current["id"])]["Q"+str(len(sets[str(user.current["id"])]))] = {"title":title, "ans":ans}
        user.current["sets"] = sets
        if request.form['button'] == "finsh":
            return redirect("/home")
    return render_template('question.html',profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

@app.route("/set")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def set():
    return render_template('set.html',profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

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
                return render_template("done.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

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
            if ans.lower() == what_ans.lower():
                return render_template('correct.html',question=question, ans=ans,profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)
            else:
                if random.randint(0,1) == 0:
                    user.current["current"].append(order[order[0]])
                return render_template('wrong.html',question=question, ans=ans,profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name) 
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
    if order[0] > len(order):
        return render_template("done.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)
    if len(fun.make_dict(user.current["sets"])[id])-1 < 3:
        question = fun.make_dict(user.current["sets"])[id]["Q"+str(order[order[0]])]["title"]
        return render_template('set2.html',question=question,profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)
    else:
        set_len = len(order)-1
        ran1 = random.randint(1,set_len)
        ran2 = random.randint(1,set_len)
        while ran1 == ran2 or order[ran1] == order[order[0]] or order[ran2] == order[order[0]] or order[ran1] == order[ran2]:
            ran1 = random.randint(1,set_len)
            ran2 = random.randint(1,set_len)
        set = fun.make_dict(user.current["sets"])[id]
        question = set["Q"+str(order[order[0]])]["title"]
        ans = [set["Q"+str(order[order[0]])]["ans"],set["Q"+str(order[ran1])]["ans"],set["Q"+str(order[ran2])]["ans"]]
        ran1 = random.randint(0,len(ans)-1);ans1 = ans[ran1];ans.pop(ran1)
        ran2 = random.randint(0,len(ans)-1);ans2 = ans[ran2];ans.pop(ran2)
        ans3 = ans[0]
        return render_template('set.html',question=question, ans1=ans1,ans2=ans2,ans3=ans3,profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name)

@app.route("/set/del/<id>")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def del_set(id):
    sets = fun.make_dict(user.current["sets"])
    del sets[id]
    user.current["sets"] = sets
    return redirect("/home")

@app.errorhandler(404)
@web.authenticated(login_res="<script>window.open('/','_self')</script>")

def page_not_found(e):
    return render_template('404.html',profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name), 404
    
@app.errorhandler(500)
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def error_500(e):
    return render_template('500.html',profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name), 500

@app.route("/community")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def community():
    pub = db["published"]
    published = {}
    deleat = []
    for i in range(len(pub)):
        try:
            set = db[pub[i][0]]["sets"][pub[i][1]]
        except:
            deleat.append(i)
        else:
            set = db[pub[i][0]]["sets"][pub[i][1]]
            published[i] = set
            db["published"][i][2] = str(i)
    for i in range(len(deleat)):
        db["published"].pop(deleat[i])
    published = fun.make_dict(published)
    print(published)
    return render_template("community.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name,published=published)

@app.route("/upload/<id>")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def upload(id):
    if int(sys.getsizeof(fun.make_dict(user.current["sets"]))) >= 4900:
        return render_template("error.html",profile_pic=request.headers["X-Replit-User-Profile-Image"],name=web.auth.name ,error_title="You have ran out of storage.",error="You have reach the max amount of storage that you have please deleat a set to make a new one.",link="/home")
    pub = db["published"]
    for i in range(len(pub)):
        if id in pub[i]:
            set = db[pub[i][0]]["sets"][pub[i][1]]
            new_id = str(user.current["id"])
            user.current["id"] =+ 1
            user.current["sets"][new_id] = set
    return redirect("/home")

@app.route("/publish/del/<id>")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def pub_del(id):
    if web.auth.name == "GoodVessel92551":
        for i in range(len(db["published"])):
            if id in db["published"][i]:
                print("Hello")
                db["published"].pop(i)
    return redirect("/community")

@app.route("/publish/<id>")
@web.authenticated(login_res="<script>window.open('/','_self')</script>")
def publish(id):
    name = web.auth.name
    id = id
    db["published"].append([name,id,0])
    return redirect("/community")

@app.route("/veiw")
def veiw():
    return fun.make_dict(user.current["sets"])

app.run(host='0.0.0.0', port=80,debug=True)