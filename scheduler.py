from pulp import *
from itertools import chain
from pprint import pprint as pp
from utilities import product_range
from constraints.Constraint import *


class Schedule:
    def __init__(self, prefs, classes, teachers):
        self.prefs = prefs
        self.classes = classes
        self.teachers = teachers
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
        self.periods = [i for i in range(7)]
        self.num_classes = [i for i in range(len(self.classes))]
        self.num_teachers = [i for i in range(len(self.teachers))]
        self.num_days = [i for i in range(len(self.days))]

    def print_data(self):
        print("PREFS:")
        print("-" * 10)
        pp(self.prefs)
        print("+" * 100)
        print("CLASSES:")
        print("-" * 10)
        pp(self.classes)
        print("+" * 100)
        print("TEACHERS:")
        print("-" * 10)
        pp(self.teachers)
        print("+" * 100)

    def build_vars(self, teachers=None, classes=None, days=None, periods=None):
        name = 0
        if not teachers:
            teachers = self.teachers
        if not classes:
            classes = self.classes
        if not days:
            days = self.days
        if not periods:
            periods = self.periods
        vars = [[[[(teacher[name], course[name], day, period)
                for teacher in teachers]
                for course in classes]
                for day in days]
                for period in periods]
        return vars

    def get_variables_list(self, matrix):
        # Flattens matrix into 1D list
        vars = list(chain.from_iterable(list(chain.from_iterable(list(chain.from_iterable(matrix))))))
        return vars

    def get_coefficient(self, tcdp):
        try:
            teacher = tcdp[0]
            course = tcdp[1][0:3]
            day = tcdp[2]
            period = tcdp[3]

            if self.prefs[teacher][course] == -1:
                return -1000
            elif self.prefs[teacher][course] == 0:
                return 1
            elif self.prefs[teacher][course] == 1:
                return 5
            else:
                return 0
        except Exception as e:
            print(e)
            print("Coefficient could not be calculated.")
            return 0

    def restructure_results(self, results):
        teacher = 0
        course = 1
        day = 2
        period = 3

        schedule_dict = {
            "Monday": [
                [], [], [], [], [], [], []
            ],
            "Tuesday": [
                [], [], [], [], [], [], []
            ],
            "Wednesday": [
                [], [], [], [], [], [], []
            ],
            "Thursday": [
                [], [], [], [], [], [], []
            ],
            "Friday": [
                [], [], [], [], [], [], []
            ]
        }

        for result in results:
            t = result[teacher]
            c = result[course]
            d = result[day]
            p = result[period]

            schedule_dict[d][p].append([c, t])

        return schedule_dict

    def build_track_classes(self):
        classes = [course for course in self.classes if course[2] == "Track"]
        periods = [2, 3, 4, 5, 6]
        t = self.num_teachers
        c = [i for i in range(len(classes))]
        d = self.num_days
        p = [i for i in range(len(periods))]
        vm = self.build_vars(classes=classes, periods=periods)
        vars = self.get_variables_list(vm)

        x = pulp.LpVariable.dicts('x', vars,
                                  lowBound=0,
                                  upBound=1,
                                  cat=pulp.LpInteger)

        schedule_model = pulp.LpProblem("Schedule", pulp.LpMaximize)
        objective = lpSum([self.get_coefficient(tcdp) * x[tcdp] for tcdp in vars])
        schedule_model += objective

        OneClassPerTeacher(t, c, d, p, x, schedule_model, vm).build()
        OneTeacherPerClass(t, c, d, p, x, schedule_model, vm).build()
        SameTeacherPerClass(t, c, d, p, x, schedule_model, vm, classes).build()
        OneTrackClassPerDay(t, c, d, p, x, schedule_model, vm).build()
        ThursdayHalfDay(t, c, d, p, x, schedule_model, vm).build()
        CorrectNumberClasses(t, c, d, p, x, schedule_model, vm, classes).build()

        schedule_model.solve()
        status = LpStatus[schedule_model.status]

        # pp(schedule_model.constraints)
        # print(schedule_model.constraints)

        selected_tcdp = []
        for tcdp in vars:
            if x[tcdp].value() == 1.0:
                selected_tcdp.append(tcdp)

        schedule = self.restructure_results(selected_tcdp)

        if status == "Infeasible":
            return status
        else:
            return schedule

    def build_schedule(self):
        var_matrix = self.build_vars()
        vars = self.get_variables_list(var_matrix)

        x = pulp.LpVariable.dicts('x', vars,
                                  lowBound=0,
                                  upBound=1,
                                  cat=pulp.LpInteger)

        schedule_model = pulp.LpProblem("Schedule", pulp.LpMaximize)
        objective = lpSum([self.get_coefficient(tcdp) * x[tcdp] for tcdp in vars])
        schedule_model += objective

        # a teacher cannot teach more than one class at a given time
        for teacher, day, period in product_range(self.num_teachers, self.num_days, self.periods):
            schedule_model += lpSum(x[var_matrix[period][day][course][teacher]] for course in self.num_classes) \
                              <= 1

        # a specific class cannot have more than one teacher
        for course, day, period in product_range(self.num_classes, self.num_days, self.periods):
            schedule_model += lpSum(x[var_matrix[period][day][course][teacher]] for teacher in self.num_teachers) \
                              <= 1

        # a track class cannot occur more than once per day and main lesson must occur in periods 1&2
        for course, day in product_range(self.num_classes, self.num_days):
            if self.classes[course][2] == "Track":
                schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                        for teacher, period in product_range(self.num_teachers, self.periods)) \
                                  <= 1
                schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                        for teacher, period in product_range(self.num_teachers, [0, 1])) \
                                  == 0
            if self.classes[course][2] == "Main Lesson":
                schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                        for teacher, period in product_range(self.num_teachers, [0, 1])) == 2
                schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                        for teacher, period in product_range(self.num_teachers, [2, 3, 4, 5, 6])) \
                                  == 0

        # each class gets one teacher
        for teacher, course in product_range(self.num_teachers, self.num_classes):
            x1 = LpVariable(name=f"x_1_{teacher}_{course}", cat="Binary")
            x2 = LpVariable(name=f"x_2_{teacher}_{course}", cat="Binary")
            schedule_model += lpSum([x1, x2]) == 1
            schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                    for day, period in product_range(self.num_days, self.periods)) - \
                              (x1 * self.classes[course][3]) <= 0
            schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                    for day, period in product_range(self.num_days, self.periods)) + \
                              (x2 * self.classes[course][3]) >= self.classes[course][3]

        # thursday is a half day
        for teacher, course in product_range(self.num_teachers, self.num_classes):
            schedule_model += lpSum(x[var_matrix[period][3][course][teacher]] for period in [4, 5, 6]) == 0

        # proper number of periods per week
        for course in self.num_classes:
            schedule_model += lpSum(x[var_matrix[period][day][course][teacher]]
                                    for teacher, day, period in product_range(self.num_teachers,
                                                                                   self.num_days,
                                                                                   self.periods)) \
                              == self.classes[course][3]

        schedule_model.solve()
        status = LpStatus[schedule_model.status]

        # pp(schedule_model.constraints)
        # print(schedule_model.constraints)

        selected_tcdp = []
        for tcdp in vars:
            if x[tcdp].value() == 1.0:
                selected_tcdp.append(tcdp)

        schedule = self.restructure_results(selected_tcdp)

        if status == "Infeasible":
            return status
        else:
            return schedule
