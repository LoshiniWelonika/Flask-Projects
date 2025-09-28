from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

#Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHMEY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app) 


#Database Model
class User(db.Model):
    #Class Variables
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(25), unique=True, nullable=False)
    password = db.column(db.String(15), primary_key=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
  



#_______________________Routes_________________________
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")








if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
