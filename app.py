from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from schedule import schedule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Название задания
    profile = db.Column(db.String(50), nullable=False)  # Профиль (ХимБио или ФизМат)
    day_of_week = db.Column(db.String(50), nullable=False)  # День недели (например, "Понедельник")
    lesson_number = db.Column(db.Integer, nullable=False)  # Номер урока
    task_description = db.Column(db.String(200), nullable=True)  # Описание задания (опционально)

    def __repr__(self):
        return f'<Task {self.name}>'

def import_schedule_to_db(schedule):
    for profile, days in schedule.items():
        for day, lessons in days.items():
            for lesson_number, lesson in enumerate(lessons, start=1):
                task = Task(
                    name=lesson["предмет"],
                    profile=profile,
                    day_of_week=day,
                    lesson_number=lesson_number,
                    task_description=f"Кабинет {lesson['кабинет']}" if lesson["кабинет"] else "Кабинет не указан"
                )
                db.session.add(task)
    db.session.commit()



with app.app_context():
    db.create_all()
    #import_schedule_to_db(schedule) #uncomment if schedule not added


@app.route('/schedule', methods=['GET'])
def get_schedule():
    profile = request.args.get('profile')
    day_of_week = request.args.get('day_of_week')

    if not profile or not day_of_week:
        return jsonify({"error": "Укажите профиль и день недели"}), 400

    day_schedule = schedule.get(profile, {}).get(day_of_week, [])
    return jsonify(day_schedule)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    profile = request.args.get('profile')
    day_of_week = request.args.get('day_of_week')

    tasks = Task.query.filter_by(profile=profile, day_of_week=day_of_week).all()
    day_schedule = schedule.get(profile, {}).get(day_of_week, [])

    return render_template('index.html', profile=profile, day_of_week=day_of_week, tasks=tasks, schedule=day_schedule)



if __name__ == '__main__':
    app.run(debug=True)