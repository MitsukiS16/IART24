import random
import numpy as np

def evaluate_solution(solution, scores):
    score = 0
    for arg in solution:
        score += int(scores[int(arg[0])])
    return score

def update_solution_score(neighbor_score, book_score, op):
    if op == "dec":
        neighbor_score -= int(book_score)
    elif op == "inc":
        neighbor_score += int(book_score)
    return neighbor_score

def replace_worst_individuals(population, offspring, scores):
    
    sorted_population = sorted(population, key=lambda x : evaluate_solution(x, scores))

    sorted_population[-len(offspring):] = offspring

    return sorted_population

def get_greatest_fit(population, scores):
    best_solution_score = evaluate_solution(population[0], scores)
    best_individual = population[0]
    current_evaluation = 0

    #print(population[1])
    for i in range(1, len(population)):
        #])
        current_evaluation = evaluate_solution(population[i], scores)
        if current_evaluation > best_solution_score:
            best_solution_score = current_evaluation
            best_individual = population[i]
    return best_individual

def tournament_select(population, tournament_size, scores, visited_parents):
    best_individual = None
    #while(True):
    #print("ts")
    participants = random.sample(population, k=tournament_size)

    best_individual = get_greatest_fit(participants, scores)

        #if tuple(best_individual) not in visited_parents: break 
    return best_individual


def roulette_select(population, total_fitness, scores, visited_parents):

    individual = None
    #while(True):
        #print("rs")
    spin_value = np.random.uniform(0, 1)
    cumulative_fitness = 0
    last_individual = None
    for individual in population:
        last_individual = individual
        cumulative_fitness += evaluate_solution(individual, scores)/total_fitness
        if cumulative_fitness >= spin_value:
            if tuple(individual) not in visited_parents:
                return individual
        #if tuple(individual) not in visited_parents: break
    return last_individual