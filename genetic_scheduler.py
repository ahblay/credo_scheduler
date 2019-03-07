import random
from pprint import pprint as pp
from deap import base
from deap import creator
from deap import tools
from itertools import chain


class GeneticScheduler:
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
        self.toolbox = base.Toolbox()
        self.vars = self.build_vars()
        self.length = self.get_genome_length()

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

    def get_genome_length(self):
        l = 0
        for c in self.classes:
            l += c[3]
        return l

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
        return list(chain.from_iterable(list(chain.from_iterable(list(chain.from_iterable(vars))))))

    def get_class_numbers(self, individual):
        classes = [c[0] for c in self.classes]
        quantity = {}
        for course in classes:
            counter = 0
            for item in individual:
                if course == item[1]:
                    counter += 1
            quantity[course] = counter
        return quantity

    def get_class_per_day(self, individual):
        for day in self.days:
            counter = 0
            for i in individual:
                pass
            pass
        pass

    def evaluate(self, individual):
        score = 100
        classes = [c for c in self.classes]
        quantity = self.get_class_numbers(individual)
        for c in classes:
            score = score - abs(quantity[c[0]] - c[3])
        return score,

    def select_var(self, vars):
        var = random.choice(vars)
        return var

    def mutate(self, individual):
        var = self.select_var(self.vars)
        idx = random.randint(0, len(individual) - 1)
        individual[idx] = var
        return individual

    def init_problem(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox.register("attr_val", self.select_var, self.vars)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.attr_val, self.length)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.evaluate)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def run(self):
        random.seed(64)

        pop = self.toolbox.population(n=300)

        CXPB, MUTPB = 0.5, 0.2

        print("Start of evolution")

        # Evaluate the entire population
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(pop))

        # Extracting all the fitnesses of
        fits = [ind.fitness.values[0] for ind in pop]

        # Variable keeping track of the number of generations
        g = 0

        # Begin the evolution
        while max(fits) < 100 and g < 100:
            # A new generation
            g = g + 1
            print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            print("  Evaluated %i individuals" % len(invalid_ind))

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x * x for x in fits)
            std = abs(sum2 / length - mean ** 2) ** 0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
        return self.restructure_results(best_ind)



