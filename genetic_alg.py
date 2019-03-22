import random
from pprint import pprint as pp
import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from itertools import product


def product_range(*args):
    return list(product(*args))

n_teachers = 10
n_classes = 10
n_days = 5
n_periods = 7

all_indices = product_range(
    range(n_teachers),
    range(n_classes),
    range(n_days),
    range(n_periods)
)
length = 40


def init_ind(icls):
    ind = np.zeros([
        n_teachers,
        n_classes,
        n_days,
        n_periods
    ])

    indices = random.sample(all_indices, length)

    for i in indices:
        ind[i[0]][i[1]][i[2]][i[3]] = 1

    return icls(ind)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", init_ind, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual):
    test_score = 0
    for course in individual[0]:
        for day in course:
            test_score += sum(list(day))
    return test_score,


# Try no crossover for simplicity
def cxTwoPointCopy(ind1, ind2):
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


def mutate(ind):
    i = random.sample(all_indices, 1)[0]
    if ind[i[0]][i[1]][i[2]][i[3]] == 1:
        ind[i[0]][i[1]][i[2]][i[3]] = 0
    else:
        ind[i[0]][i[1]][i[2]][i[3]] = 1
    return ind


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", cxTwoPointCopy)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)


def compare_ndarrays(a1, a2):
    return False

def main():
    random.seed(64)

    pop = toolbox.population(n=300)
    #pp(pop[0])

    # Numpy equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # numpy.array_equal or numpy.allclose solve this issue.
    hof = tools.HallOfFame(1, similar=compare_ndarrays)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=30, stats=stats,
                        halloffame=hof)

    return pop, stats, hof


if __name__ == "__main__":
    pop, stats, hof = main()
    best_ind = tools.selBest(pop, 1)[0]
    print(best_ind)