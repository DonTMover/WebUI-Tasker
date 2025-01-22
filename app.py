from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Название задания
    profile = db.Column(db.String(50), nullable=False)  # Профиль (ХимБио или ФизМат)
    day_of_week = db.Column(db.String(50), nullable=False)  # День недели (например, "Понедельник")
    task_description = db.Column(db.String(200), nullable=True)  # Описание задания (опционально)

    def __repr__(self):
        return f'<Task {self.name}>'


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    profile = request.args.get('profile')
    day_of_week = request.args.get('day_of_week')

    tasks = Task.query.filter_by(profile=profile, day_of_week=day_of_week).all()

    return render_template('index.html', profile=profile, day_of_week=day_of_week, tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)