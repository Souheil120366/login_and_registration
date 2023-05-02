from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return redirect('/dashboard')

@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate_user(request.form):
        # redirect to the route where the dojo form is rendered.
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['pwd'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "pwd" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    print("user_id here",user_id)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/success")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['pwd']):
        # if we get False after checking the password
        flash("Invalid Email/Password","login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/success")

@app.route("/success")
def user_show():
    if 'user_id' not in session:
        return redirect ("/dashboard")
    user_to_show = User.get_one({'id':session['user_id']})
    return render_template("success.html",user=user_to_show)
    

@app.route('/dashboard')
def create_user():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/dashboard')
