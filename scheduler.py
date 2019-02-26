import pulp
from itertools import chain
from pprint import pprint as pp


class Schedule:
    def __init__(self, prefs, classes, teachers):
        self.prefs = prefs
        self.classes = classes
        self.teachers = teachers
        self.periods = [i for i in range(32)]

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

    def build_vars(self):
        name = 0
        vars = [[[(teacher[name], course[name], period) for teacher in self.teachers]
                for course in self.classes]
                for period in self.periods]
        return vars

    def get_variables_list(self, matrix):
        # Flattens matrix into 1D list
        vars = (list(chain.from_iterable(list(chain.from_iterable(matrix)))))
        return vars

    def build_schedule(self):
        vars = self.get_variables_list(self.build_vars())
        pp(vars)

