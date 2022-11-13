from flask import Flask, request, redirect, url_for, render_template
from verify_signin import ver
from register_users import ad 
from user_health import add_health, retrieve
from user_medicines import list_meds, add_meds, remove_med, remind

app = Flask(__name__)

@app.route('/')
def default():
    return redirect(url_for("home"))

@app.route('/contact')
def contact():
    return render_template("contact.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "POST":
        action = request.form["action"]
        if action == "Register":
            return redirect(url_for("register"))
        else: 
            return redirect(url_for("signin"))
    else:
        return render_template("home.html")

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        usr = "User"
        user = request.form["nm"]
        password = request.form['key']
        cpassword = request.form['ckey']
        email = request.form['em']
        if password == cpassword:
            if(ad(user,password,email,usr)):
                add_health(user,"","","","","","","")
                add_meds(user,"",0,0,0,0,0,0,0)
                return redirect(url_for("f_signin"))
            else:
                return render_template("register.html",alreadyexists = "Username is already taken!", mismatch = "",un = user, pas = password, em = email)
        else:
            return render_template("register.html", alreadyexists = "", mismatch = "Passwords do not match !",un = user, pas = password, em = email)

    else: 
        return render_template("register.html",alreadyexists = "", mismatch = "",un = "", pas = "", em = "")    

@app.route('/f_signin', methods=['POST','GET'])
def f_signin():
    if request.method == "POST":
        usr = "User"
        user = request.form["nm"]
        password = request.form['key']
        if ver(usr,user,password) == "Verified":
            username = user
            return redirect(url_for("main",username = username)) 
        else:
            return render_template("signin.html", inv = "Invalid Username or password ! Re-enter the correct credentials.")        
    else: 
        return render_template("signin.html",inv = "")    

@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method == "POST":
        usr = "User"
        user = request.form["nm"]
        password = request.form['key']
        if ver(usr,user,password) == "Verified":
            username = user
            return redirect(url_for("profile",username = username)) 
        else:
            return render_template("signin.html", inv = "Invalid Username or password ! Re-enter the correct credentials.")        
    else: 
        return render_template("signin.html",inv = "")    

@app.route('/profile/<username>', methods=['POST','GET'])
def profile(username):
    res = retrieve(username)
    medicines = list_meds(username)
    queue = remind(username)
    if request.method == "POST":
        button_clicked = request.form['submit_button']
        if button_clicked == 'update health':
            return redirect(url_for("main",username = username)) 
        elif button_clicked == 'set reminder':
            return redirect(url_for("addMeds",username = username)) 
    else:
        return render_template("profile.html",nm = res[0],age = res[1], gen = res[2], h = res[3], w = res[4], bg = res[5], all = res[6], hc = res[7],medicines = medicines,queue = queue)

@app.route('/main/<username>', methods=['POST','GET'])
def main(username):
    res = retrieve(username)
    if request.method == "POST":
        age = request.form["age"]
        gen = request.form['gend']
        h = request.form['h']
        w = request.form['w']
        bg = request.form['bloodg']
        all = request.form['all']
        hc = request.form['hc']
        add_health(username,age,gen,h,w,bg,all,hc)
        return redirect(url_for("profile",username = username)) 
    else:
        return render_template("HealthSetup.html",age = res[1], h = res[3], w = res[4], all = res[6], hc = res[7])

@app.route('/addMeds/<username>', methods=['POST','GET'])
def addMeds(username):
    medicines  = list_meds(username)
    if request.method == "POST":
        button_clicked = request.form['add_delete']
        if button_clicked == 'delete':
            med = request.form["med_del"]
            remove_med(username,med)
        elif button_clicked == 'add':
            med = request.form["med"]
            days = request.form['days']
            d_mor = request.form['d_mor']
            d_noon = request.form['d_noon']
            d_night = request.form['d_night']
            t_mor = request.form['t_mor']
            t_noon = request.form['t_noon']
            t_night = request.form['t_night']
            if (d_mor == 0 and t_mor != "") or (d_noon == 0 and t_noon != "") or (d_night == 0 and t_night != ""):
                return redirect(url_for("profile",username = username)) 
            if med != "" and days != 0:
                add_meds(username,med,days,d_mor,d_noon,d_night,t_mor,t_noon,t_night)
        return redirect(url_for("profile",username = username)) 
    else:
        return render_template("Medicines.html",medicines = medicines)
if __name__ == "__main__" :
    app.run(debug = True)
