import random
from pprint import pprint as pp
import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from itertools import product


class Genetic:
    def __init__(self, prefs, classes, teachers):
        self.prefs = prefs
        self.classes = classes
        self.teachers = teachers
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.periods = [i for i in range(7)]
        self.n_classes = len(classes)
        self.n_teachers = len(teachers)
        self.n_days = 5
        self.n_periods = 7
        self.all_indices = self.product_range(
                                range(self.n_teachers),
                                range(self.n_classes),
                                range(self.n_days),
                                range(self.n_periods)
                            )
        self.length = self.get_genome_length()
        self.toolbox = base.Toolbox()

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

    def product_range(self, *args):
        return list(product(*args))

    def get_genome_length(self):
        l = 0
        for c in self.classes:
            l += c[3]
        return l

    def decode_ind(self, ind):
        t, c, d, p = -1, -1, -1, -1
        data = []

        for teacher in ind:
            t += 1
            for course in teacher:
                c = (c + 1) % self.n_classes
                for day in course:
                    d = (d + 1) % self.n_days
                    for period in day:
                        p = (p + 1) % self.n_periods
                        if period == 1:
                            data.append((self.teachers[t][0],
                                         self.classes[c][0],
                                         self.days[d],
                                         self.periods[p]
                                         ))

        return data

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

    def init_ind(self, icls):
        ind = np.zeros([
            self.n_teachers,
            self.n_classes,
            self.n_days,
            self.n_periods
        ])

        indices = random.sample(self.all_indices, self.length)

        for i in indices:
            ind[i[0]][i[1]][i[2]][i[3]] = 1

        return icls(ind)

    def evalOneMax(self, individual):
        test_score = 0
        for course in individual[0]:
            for day in course:
                test_score += sum(list(day))
        return test_score,

    # Try no crossover for simplicity
    def cxTwoPointCopy(self, ind1, ind2):
        '''size = len(ind1)
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:  # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
            = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()'''

        return ind1, ind2

    def mutate(self, ind):
        i = random.sample(self.all_indices, 1)[0]
        if ind[i[0]][i[1]][i[2]][i[3]] == 1:
            ind[i[0]][i[1]][i[2]][i[3]] = 0
        else:
            ind[i[0]][i[1]][i[2]][i[3]] = 1
        return ind

    def init_problem(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

        self.toolbox.register("individual", self.init_ind, creator.Individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evalOneMax)
        self.toolbox.register("mate", self.cxTwoPointCopy)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def compare_ndarrays(self, a1, a2):
        return False

    def run(self):
        random.seed(64)

        pop = self.toolbox.population(n=300)
        # pp(pop[0])

        # Numpy equality function (operators.eq) between two arrays returns the
        # equality element wise, which raises an exception in the if similar()
        # check of the hall of fame. Using a different equality function like
        # numpy.array_equal or numpy.allclose solve this issue.
        hof = tools.HallOfFame(1, similar=self.compare_ndarrays)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=300, stats=stats,
                            halloffame=hof)

        best_ind = tools.selBest(pop, 1)[0]
        pp(self.decode_ind(best_ind))

        return self.restructure_results(self.decode_ind(best_ind))
