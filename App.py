from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/to_do'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MySQL table model
class Add(db.Model):
    __tablename__ = 'add'

    empid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emptask = db.Column(db.String(200))
    empcomplate = db.Column(db.Boolean, default=False)


# Create table (only first time)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    tasks = Add.query.all()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get("task")

    if task_text:
        new_task = Add(emptask=task_text)
        db.session.add(new_task)
        db.session.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Add.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/toggle/<int:id>')
def toggle_task(id):
    task = Add.query.get(id)
    task.empcomplate = not task.empcomplate
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
