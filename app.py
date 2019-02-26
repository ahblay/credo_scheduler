import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from scheduler import Schedule

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.add_extension('jinja2.ext.do')
db = SQLAlchemy(app)

from utilities import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_teachers', methods=['GET', 'POST'])
def add_teachers():
    teachers = []
    if request.method == "GET":
        teachers = get_teachers()

    if request.method == "POST":
        name = request.form['name']
        classes = request.form["classes"].split(", ")
        primary = to_boolean(request.form["full_time"])

        update_teachers(db, name, classes, primary)

    return render_template('add_teachers.html', teachers=teachers)


@app.route('/add_classes', methods=['GET', 'POST'])
def add_classes():
    classes = []
    if request.method == 'GET':
        classes = get_classes()

    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        type = request.form['type']
        hours = request.form['hours']

        update_classes(db, name, subject, type, hours)

    return render_template('add_classes.html', classes=classes)


@app.route('/prefs', methods=['GET', 'POST'])
def enter_prefs():
    prefs = {}
    classes = []
    teachers = []
    if request.method == 'GET':
        prefs = get_prefs()
        classes = get_classes()
        teachers = get_teachers()

    if request.method == 'POST':
        # post updated preferences to database
        teacher_name = request.form["teacher"]
        class_name = request.form["class"]
        pref = request.form["pref"]
        update_prefs(db, teacher_name, class_name, pref)

    return render_template('prefs.html', prefs=prefs, classes=classes, teachers=teachers)


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        prefs = get_prefs()
        classes = get_classes()
        teachers = get_teachers()
        s = Schedule(prefs, classes, teachers)
        s.print_data()
        s.build_schedule()
    return render_template('schedule.html')


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        item = request.form["item"]
        table_name = request.form["table_name"]
        if table_name == "teachers":
            to_delete = Teachers.query.filter_by(name=item).all()
            for i in to_delete:
                db.session.delete(i)
                db.session.commit()
        if table_name == "classes":
            to_delete = Classes.query.filter_by(name=item).all()
            for i in to_delete:
                db.session.delete(i)
                db.session.commit()
        if table_name == 'class_prefs':
            pass
        else:
            return f" Failed to remove {item} from {table_name}."
    return f"Removed {item} from {table_name}."


@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run()
