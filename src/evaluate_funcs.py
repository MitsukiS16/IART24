import random
import numpy as np
import math as m
from concurrent.futures import ProcessPoolExecutor, as_completed


def evaluate_population(population, scores):
    individual_to_future = {}
    
    total_fitness = 0
    best_score = 0
    best_solution = None
    with ProcessPoolExecutor() as executor:
        for individual in population:
            individual_key = tuple(individual)
            future = executor.submit(evaluate_solution, individual, scores)
            individual_to_future[individual_key] = future

        for future in as_completed(individual_to_future.values()):  
            individual = {v: k for k, v in individual_to_future.items()}[future]
            try:
                fitness_score = future.result() 
                individual_to_future[individual] = future.result()
                total_fitness += fitness_score
                if fitness_score > best_score:
                    best_score = fitness_score
                    best_solution = list(individual)
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    return total_fitness, best_score, best_solution, individual_to_future

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

def hybrid_elitism(len_old_population, new_population, old_individuals_scores , elite_percentage):

    num_elites = int(len_old_population * elite_percentage)

    sorted_individuals = sorted(old_individuals_scores.keys(), key=lambda ind: old_individuals_scores[ind], reverse=True)

    elites = sorted_individuals[:num_elites]

    mixed_population = elites + new_population[:len_old_population - num_elites]

    return mixed_population

def get_greatest_fit(population, scores):

    _, _, best_solution, _ = evaluate_population(population, scores)
    return best_solution

def tournament_select(population, tournament_size, scores):
    participants = random.sample(population, k=tournament_size)

    best_individual = max(participants, key=lambda ind: evaluate_solution(ind, scores))

    return list(best_individual)

def roulette_select(total_fitness, old_scores_individuals):

    spin_value = np.random.uniform(0, 1)
    cumulative_fitness = 0
    last_individual = None

    for individual, score in old_scores_individuals.items():
        last_individual = individual
        cumulative_fitness += m.floor(score / total_fitness)
        if cumulative_fitness >= spin_value:
            return list(individual)
    return list(last_individual)

def evaluate_library_efficiency(sign_up_time, shipping_days, shipping_time):
    return (shipping_days - sign_up_time) * shipping_time, shipping_days