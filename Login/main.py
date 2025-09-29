from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth 
from api_key import *


app = Flask(__name__)
app.secret_key = "your_secret_key"

#Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app) 


oauth = OAuth(app) 

google = oauth.register(
    name = 'google',
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    server_metadata_uri='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope': 'openid profile email'}
) 



#Database Model
class User(db.Model):
    #Class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
  



#_______________________Routes_________________________
@app.route("/")
def home():
    return render_template("index.html")



@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first() 

    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")
    



@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first() 
    if user:
        return render_template("index.html", error="User already exists")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html", username=session['username'])
    else:
        return redirect(url_for('home'))
    
@app.route("/logout")
def logout():
    session.pop('usename', None)
    return redirect(url_for('home')) 

#Login for google
@app.route('/login/google')
def login_google():
    try:
        redirect_uri = url_for("authorize", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f"Error during login:{str(e)}")
        return "Error occured during login", 500 


#Authoirze for google
@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    userinfo_endpoint = google.server_metadata['userinfo_endpoint'] 
    resp = google.get(userinfo_endpoint)
    user_info = resp.json()
    username = user_info['email']

    user = User.query.filter_by(username=username).first() 
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    session['oauth_token'] = token

    return redirect(url_for('dashboard'))








#Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
