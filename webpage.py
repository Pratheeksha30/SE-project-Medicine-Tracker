from flask import Flask, request, redirect, url_for, render_template
from verify_signin import ver
from register_users import ad

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
                return redirect(url_for("f_signin"))
            else:
                return render_template("register.html",alreadyexists = "Username is already taken!", mismatch = "",un = user, pas = password, em = email)
        else:
            return render_template("register.html", alreadyexists = "", mismatch = "Passwords do not match !",un = user, pas = password, em = email)

    else: 
        return render_template("register.html",alreadyexists = "", mismatch = "",un = user, pas = password, em = email)    

@app.route('/f_signin', methods=['POST','GET'])
def f_signin():
    if request.method == "POST":
        usr = "User"
        user = request.form["nm"]
        password = request.form['key']
        if ver(usr,user,password) == "Verified":
            return redirect(url_for("main")) 
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
            return redirect(url_for("profile")) 
        else:
            return render_template("signin.html", inv = "Invalid Username or password ! Re-enter the correct credentials.")        
    else: 
        return render_template("signin.html",inv = "")    

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == "POST":
        return render_template("Prescriptions.html")
    else:
        return render_template("Prescriptions.html")

@app.route('/main', methods=['POST','GET'])
def main():
    if request.method == "POST":
        return render_template("HealthSetup.html")
    else:
        return render_template("HealthSetup.html")

if __name__ == "__main__" :
    app.run(debug = True)
