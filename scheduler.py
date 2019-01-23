import pulp
from datetime import timedelta, date


class Scheduler:
    def __init__(self, courses, days, periods):
        self.courses = courses
        self.days = days
        self.periods = periods

    def build_varaibles(self):
        vars = [(course, day, period) for course in self.courses
                for day in self.days
                for period in self.periods]
        return vars

    def build_model(self):
        return


def date_range(start, end):
    dates = []
    for n in range(int((start - end).days) + 1):
        dates.append(start + timedelta(n))
    return dates

courses = ["MAT01", "MAT02", "HUM01", "HUM02", "HUM03", "PHY01", "PHY02", "PHY03"]
start = date(2015, 12, 20)
end = date(2016, 1, 11)
days = date_range(start, end)
print(days)
periods = [7, 7, 7, 4, 7]
s = Scheduler(courses, days, periods)

