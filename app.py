from flask import Flask, redirect, render_template, request, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# /// -> relatie path , //// -> absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # database has been initalized


# making a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # false because we dont want user to leftt empty
    content = db.Column(db.String(200), nullable=False)  # text column
    completed = db.Column(db.Integer, default=0)  # when compleated
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There is an issue adding your Task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# route for deleting task


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a poblem while deleting your TODO'

# route for updating task


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
