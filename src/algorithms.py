########################################
### Initial Solutions
# Random Solution
# Trivial Solution
# Greedy Constrution

### Algorithms to implement
# [Metaheuristic Methods] Genetic [Anotations on PP3]
# [Metaheuristic Methods] Simulated Annealing [Anotations on PP3]
# [Metaheuristic Methods] Tabu Search [Anotations on PP3]
# [Metaheuristic Methods] Guided Local Search [Anotations on PP3]
# [Metaheuristic Methods] Particle Swarm Optimization
# [Iterative Methods] Gradient Descent
# [Iterative Methods] Newton's Method
# [Iterative Methods] Conjugate Gradient Method
# [Analytical Methods] Calculus-based Optimization
# [Analytical Methods] Linear Programming
# [Derivative-Free Optimization] Pattern Search
# [Derivative-Free Optimization] Nelder-Mead Method
# [Derivative-Free Optimization] Evolutionary Strategies

########################################
# Imports 
from library import Library
from parser import read_data
import numpy as np
import copy

########################################
# Global Variables
libraries_shipped = set()
libraries = {}
scores = []
i = 0
books = {}
libID = 0
islib = False
diffbooks = None
numLibs = None
shipping_days = None


########################################
# Function to get the id of the initial solution

# Random initial solution
def get_random_solution():
    print("##################################")
    print("You enter the get_random_solution Function")
    print("##################################")

    #TO DO 


    return 0

# Trivial initial solution
def get_trivial_solution():
    print("##################################")
    print("You enter the get_trivial_solution Function")
    print("##################################")

    #TO DO 

    return 0

# Gready initial solution
def get_greedy_solution():
    print("##################################")
    print("You enter the get_greedy_solution Function")
    print("##################################")

    #TO DO 

    return 0

########################################
# Helper function to print algorithm information
def print_info(alg_name,file_path,init_solution_name,score):
    print("-------------------------------------------------------------")
    print(f"| Algorithm: {alg_name}")
    print(f"| File: {file_path}")
    print(f"| Initial Solution: {init_solution_name}")
    print(f"| The final score was: {score}")
    print("-------------------------------------------------------------")

########################################
# Algorithms

# Algorithm 3
def algorithm3(file_path,id_init_sol,init_solution_name):
    print("##################################")
    print("You enter the algorithm3 Function")
    print("##################################")

    # Initialization of Variables
    alg_name = "Algorithmo 3 :)"
    score = 0
    
    # Read library

    # Get Initial Solution

    # Get Score


    # Return Information to Menu
    print_info(alg_name,file_path,init_solution_name,score)
    return 0



# Algorithm 2
def algorithm2(file_path,id_init_sol,init_solution_name):
    print("##################################")
    print("You enter the algorithm2 Function")
    print("##################################")

    # Initialization of Variables
    alg_name = "Algorithmo 2 :)"
    score = 0
    
    # Read library

    # Get Initial Solution

    # Get Score


    # Return Information to Menu
    print_info(alg_name,file_path,init_solution_name,score)
    return 0





# Algorithm 1
def algorithm1(file_path,id_init_sol,init_solution_name):
    print("##################################")
    print("You enter the algorithm1 Function")
    print("##################################")

    # Initialization of Variables
    alg_name = "Algorithmo 1 :)"
    score = 0
    
    # Read library

    # Get Initial Solution

    # Get Score


    # Return Information to Menu
    print_info(alg_name,file_path,init_solution_name,score)
    return 0


