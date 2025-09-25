from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuration
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///students.db'
db = SQLAlchemy(app) 


#Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False) 
    age = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String, default="gmail.com")

    def __repr__(self):
        return f"<Student {self.id}>" 
    

#Create DB file if not exists
with app.app_context():
    db.create_all()



#Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    #Add a Task
    if request.method == 'POST':
        student_name = request.form['name']
        student_age = request.form['age']
        student_email = request.form['email']
        new_details = Student(name=student_name, age=student_age, email=student_email)
        try:
            db.session.add(new_details)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return str(e)
    
    #See all details
    else:
        students = Student.query.order_by(Student.id).all() 

    
    return render_template("index.html", students=students) 
        

#Delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_student = Student.query.get_or_404(id)
    try:
        db.session.delete(delete_student)
        db.session.commit()
        return redirect("/")
    except Exception as e:
            print(e)
            return str(e)
    

#Edit and item
@app.route("/update/<int:id>", methods=["GET", 'POST']) 
def edit(id:int):
    student = Student.query.get_or_404(id) 
    if request.method == "POST":
        student.name = request.form['name']
        student.age = request.form['age']
        student.email = request.form['email']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return str(e)
    else:
        return render_template('edit.html', student=student) 



#Run Server
if __name__ == '__main__':
    app.run(debug=True)

