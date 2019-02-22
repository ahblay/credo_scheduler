import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Teachers, Classes, ClassPrefs


def to_boolean(string):
    if string == "true":
        return True
    else:
        return False


@app.route('/add_teachers', methods=['GET', 'POST'])
def add_teachers():
    teachers = []
    if request.method == "GET":
        for teacher in Teachers.query.all():
            if teacher.name:
                data = [teacher.name, teacher.classes]
                teachers.append(data)

    if request.method == "POST":
        name = request.form['name']
        classes = request.form["classes"].split(", ")
        primary = to_boolean(request.form["full_time"])
        print(request.form['full_time'])
        print(name, classes, primary)

        try:
            to_update = Teachers.query.filter_by(name=name).first()
            if not to_update:
                result = Teachers(
                    name=name,
                    classes=classes,
                    primary=primary
                )
                db.session.add(result)
                db.session.commit()
            else:
                to_update.classes = classes
                to_update.primary = primary
                db.session.commit()
        except Exception as e:
            print(e)
            print("Could not add to database")

    return render_template('add_teachers.html', teachers=teachers)


@app.route('/add_classes', methods=['GET', 'POST'])
def add_classes():
    courses = []
    if request.method == 'GET':
        classes = Classes.query.all()
        for course in classes:
            data = [course.name, course.subject, course.type, course.hours]
            courses.append(data)

    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        type = request.form['type']
        hours = request.form['hours']

        try:
            to_update = Classes.query.filter_by(name=name).first()
            if not to_update:
                result = Classes(
                    name=name,
                    subject=subject,
                    type=type,
                    hours=hours
                )
                db.session.add(result)
                db.session.commit()
            else:
                to_update.subject = subject
                to_update.type = type
                to_update.hours = hours
                db.session.commit()
        except Exception as e:
            print(e)
            print("Failed to update class.")
    return render_template('add_classes.html', classes=courses)


@app.route('/prefs', methods=['GET', 'POST'])
def enter_prefs():
    class_prefs = {}
    if request.method == 'GET':
        # get preference data from database
        prefs = ClassPrefs.query.order_by(ClassPrefs.teacher_name).all()
        for pref in prefs:
            print(pref.teacher_name, pref.class_name, pref.pref)
            if pref.teacher_name in class_prefs:
                class_prefs[pref.teacher_name][pref.class_name] = pref.pref
            else:
                class_prefs[pref.teacher_name] = {}
                class_prefs[pref.teacher_name][pref.class_name] = pref.pref
        print(class_prefs)

    if request.method == 'POST':
        # post updated preferences to database
        teacher_name = request.form["teacher"]
        class_name = request.form["class"]
        pref = request.form["pref"]

        print(teacher_name, class_name, pref)

        try:
            to_update = ClassPrefs.query.filter_by(teacher_name=teacher_name, class_name=class_name).first()
            print(to_update)
            if not to_update:
                result = ClassPrefs(
                    teacher_name=teacher_name,
                    class_name=class_name,
                    pref=pref
                )
                db.session.add(result)
                db.session.commit()
            else:
                to_update.pref = pref
                print("Updated database with pref data.")
                db.session.commit()
        except Exception as e:
            print(e)
            print("Could not update database.")

    return render_template('prefs.html', prefs=class_prefs)


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
            pass
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
