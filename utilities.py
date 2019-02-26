from models import *


def to_boolean(string):
    if string == "true":
        return True
    else:
        return False


def get_teachers():
    teachers = []
    for teacher in Teachers.query.all():
        if teacher.name:
            data = [teacher.name, teacher.classes]
            teachers.append(data)
    return teachers


def get_classes():
    courses = []
    for course in Classes.query.all():
        data = [course.name, course.subject, course.type, course.hours, course.code]
        courses.append(data)
    return courses


def get_prefs():
    prefs = {}
    for pref in ClassPrefs.query.order_by(ClassPrefs.teacher_name).all():
        if pref.teacher_name in prefs:
            prefs[pref.teacher_name][pref.class_name] = pref.pref
        else:
            prefs[pref.teacher_name] = {}
            prefs[pref.teacher_name][pref.class_name] = pref.pref
    return prefs


def update_teachers(db, name, courses, primary):
    try:
        to_update = Teachers.query.filter_by(name=name).first()
        if not to_update:
            result = Teachers(
                name=name,
                classes=courses,
                primary=primary
            )
            db.session.add(result)
            db.session.commit()
        else:
            to_update.classes = courses
            to_update.primary = primary
            db.session.commit()
    except Exception as e:
        print(e)
        print("Could not add to database")


def update_classes(db, name, subject, type, hours):
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


def update_prefs(db, teacher_name, class_name, pref):
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