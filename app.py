from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

# My App Setup
app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_todo.db'
db = SQLAlchemy(app)


# Data Class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'Task {self.id}'


@app.route('/', methods=['POST', 'GET'])
def index():
    # Add a Task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'ERROR:{e}')
            return f'ERROR:{e}'
    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
