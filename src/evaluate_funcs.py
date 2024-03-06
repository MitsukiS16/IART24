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
    best_solution = evaluate_solution(population[0], scores)
    best_individual = population[0]

    for individual in population[1:]:
        current_evaluation = evaluate_solution(individual, scores)
        if current_evaluation > best_solution:
            best_solution = current_evaluation
            best_individual = individual
    return best_individual

def tournament_select(population, tournament_size, scores):
    participants = random.sample(population, k=tournament_size)

    best_individual = get_greatest_fit(participants, scores)
    
    return best_individual


def roulette_select(population, total_fitness, scores):
    spin_value = np.random.uniform(0, 1)
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += evaluate_solution(individual, scores)/total_fitness
        if cumulative_fitness >= spin_value:
            return individual