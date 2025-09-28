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




#Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
