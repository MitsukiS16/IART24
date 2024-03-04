def evaluate_solution(solution, scores):
    score = 0
    for arg in solution:
        score += int(scores[int(arg[0])])
    return score

def replace_worst_individuals(population, offspring):
    
    sorted_population = sorted(population, key=evaluate_solution)

    sorted_population[-len(offspring):] = offspring

    return sorted_population
