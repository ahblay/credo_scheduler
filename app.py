import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Teacher


def toBoolean(string):
    if string == "true":
        return True
    else:
        return False


@app.route('/add_teachers', methods=['GET', 'POST'])
def index():
    errors = []
    print("In index")
    if request.method == "POST":
        names = request.form.getlist('names[]')
        classes = request.form.getlist("classes[]")
        full_time = request.form.getlist("full_time[]")
        teacher_data = list(zip(names, classes, full_time))
        print(teacher_data)

        try:
            for teacher in teacher_data:
                name = teacher[0]
                classes = teacher[1].split(", ")
                primary = toBoolean(teacher[2])
                result = Teacher(
                    name=name,
                    classes=classes,
                    primary=primary
                )
                db.session.add(result)
            db.session.commit()
        except Exception as e:
            print(e)
            print("Could not add to database")

    return render_template('index.html', errors=errors)


@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run()
