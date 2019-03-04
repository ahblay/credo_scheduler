from pulp import lpSum
from utilities import product_range
from pulp import LpVariable


class Constraint:
    def __init__(self, t, c, d, p, x, prob, vm):
        self.t = t
        self.c = c
        self.d = d
        self.p = p
        self.x = x
        self.prob = prob
        self.vm = vm


class OneClassPerTeacher(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm):
        self.description = "A teacher cannot teach more than one class at a given time."
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for teacher, day, period in product_range(self.t, self.d, self.p):
            self.prob += lpSum(self.x[self.vm[period][day][course][teacher]] for course in self.c) <= 1


class OneTeacherPerClass(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm):
        self.description = "A specific class cannot have more than one teacher."
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for course, day, period in product_range(self.c, self.d, self.p):
            self.prob += lpSum(self.x[self.vm[period][day][course][teacher]] for teacher in self.t) <= 1


class SameTeacherPerClass(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm, classes):
        self.description = "Each class gets one teacher per scheduling period."
        self.classes = classes
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for teacher, course in product_range(self.t, self.c):
            x1 = LpVariable(name=f"x_1_{teacher}_{course}", cat="Binary")
            x2 = LpVariable(name=f"x_2_{teacher}_{course}", cat="Binary")
            self.prob += lpSum([x1, x2]) == 1
            self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                    for day, period in product_range(self.d, self.p)) - \
                              (x1 * self.classes[course][3]) <= 0
            self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                    for day, period in product_range(self.d, self.p)) + \
                              (x2 * self.classes[course][3]) >= self.classes[course][3]


class OneTrackClassPerDay(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm, classes):
        self.description = "A track class cannot occur more than once per day."
        self.classes = classes
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for course, day in product_range(self.c, self.d):
            if self.classes[course][2] == "Track":
                self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                   for teacher, period in product_range(self.t, self.p)) <= 1


class ThursdayHalfDay(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm):
        self.description = "Thursday is a half day."
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for teacher, course in product_range(self.t, self.c):
            self.prob += lpSum(self.x[self.vm[period][3][course][teacher]] for period in [2, 3, 4]) == 0


class CorrectNumberClasses(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm, classes):
        self.description = "Correct number of classes per week."
        self.classes = classes
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for course in self.c:
            self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                               for teacher, day, period in product_range(self.t, self.d, self.p)) \
                        == self.classes[course][3]


class MainLessonPeriods(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm, classes):
        self.description = "Main lesson occurs in periods one and two."
        self.classes = classes
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for course, day in product_range(self.c, self.d):
            if self.classes[course][2] == "Main Lesson":
                self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                   for teacher, period in product_range(self.t, [0, 1])) == 2
                self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                   for teacher, period in product_range(self.t, [2, 3, 4, 5, 6])) == 0


class TrackClassPeriods(Constraint):
    def __init__(self, t, c, d, p, x, prob, vm, classes):
        self.description = "A track class cannot occur more than once per day."
        self.classes = classes
        super().__init__(t, c, d, p, x, prob, vm)

    def info(self):
        print(self.description)

    def build(self):
        for course, day in product_range(self.c, self.d):
            if self.classes[course][2] == "Track":
                self.prob += lpSum(self.x[self.vm[period][day][course][teacher]]
                                   for teacher, period in product_range(self.t, [0, 1])) == 0
