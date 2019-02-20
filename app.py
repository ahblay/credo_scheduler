import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Teachers, ClassPrefs


def to_boolean(string):
    if string == "true":
        return True
    else:
        return False


@app.route('/add_teachers', methods=['GET', 'POST'])
def add_teachers():
    errors = []
    if request.method == "POST":
        names = request.form.getlist('names[]')
        classes = request.form.getlist("classes[]")
        full_time = request.form.getlist("full_time[]")
        teacher_data = list(zip(names, classes, full_time))

        try:
            for teacher in teacher_data:
                name = teacher[0]
                classes = teacher[1].split(", ")
                primary = to_boolean(teacher[2])
                result = Teachers(
                    name=name,
                    classes=classes,
                    primary=primary
                )
                db.session.add(result)
            db.session.commit()
        except Exception as e:
            print(e)
            print("Could not add to database")

    return render_template('add_teachers.html', errors=errors)


@app.route('/add_classes')
def add_classes():
    return render_template('add_classes.html')


@app.route('/prefs', methods=['GET', 'POST'])
def enter_prefs():
    prefs = {}
    if request.method == 'GET':
        # get preference data from database
        prefs = ClassPrefs.query.all()
        print(prefs)
    if request.method == 'POST':
        # post updated preferences to database
        teacher_name = request.form["teacher"]
        class_name = request.form["class"]
        pref = request.form["pref"]

        print(teacher_name, class_name, pref)

        try:
            toUpdate = ClassPrefs.query.filter_by(teacher_name=teacher_name, class_name=class_name).all()
            print(toUpdate)
            if not toUpdate:
                result = ClassPrefs(
                    teacher_name=teacher_name,
                    class_name=class_name,
                    pref=pref
                )
                db.session.add(result)
                db.session.commit()
            else:
                toUpdate.pref = pref
                print("Updated database with pref data.")
                db.session.commit()
        except Exception as e:
            print(e)
            print("Could not update database.")

    return render_template('prefs.html', prefs=prefs)


@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run()
