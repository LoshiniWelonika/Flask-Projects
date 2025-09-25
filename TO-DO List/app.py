#Imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#My-APP
app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app) 


#Data Class ~ Row of Data 
class Task (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"Task {self.id}"
    
with app.app_context():
        db.create_all()

#Routes to web pages
@app.route("/", methods=["POST","GET"])
def index():
    #Add a Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return str(e)

    #See all current tasks
    else:
        tasks = Task.query.order_by(Task.created).all() 



    return render_template("index.html", tasks=tasks)



#Delete an item
@app.route("/delete/<int:id>") 
def delete(id:int):
    delete_task = Task.query.get_or_404(id) 
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
            print(e)
            return str(e)


#Edit an item
@app.route("/update/<int:id>", methods=["GET", 'POST']) 
def edit(id:int):
    task = Task.query.get_or_404(id) 
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return str(e)
    else:
        return render_template('edit.html', task=task) 



if __name__ == "__main__":
    app.run(debug=True)