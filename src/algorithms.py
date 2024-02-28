# Algorithm Functions

# Sugestoes de algoritmos para implementar: (5 primeiros +importantes, os outros fazemos dependendo do tempo que temos :P)

### Initial Solutions
# Random Solution
# Trivial Solution
# Greedy Constrution

### Algorithms to implement
# [Metaheuristic Methods] Genetic
# [Metaheuristic Methods] Simulated Annealing
# [Metaheuristic Methods] Particle Swarm Optimization
# [Iterative Methods] Gradient Descent
# [Iterative Methods] Newton's Method
# [Iterative Methods] Conjugate Gradient Method
# [Analytical Methods] Calculus-based Optimization
# [Analytical Methods] Linear Programming
# [Derivative-Free Optimization] Pattern Search
# [Derivative-Free Optimization] Nelder-Mead Method
# [Derivative-Free Optimization] Evolutionary Strategies

# Escolher um algoritmos, criar o codigo e ver score :) simples :P




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
# Main and Auxiliar Functions for Optimization Algorithms


# Helper function to print algorithm information
def print_info(alg_name,file_path,init_solution,score):
    print("-------------------------------------------------------------")
    print(f"| Algorithm: {alg_name}")
    print(f"| File: {file_path}")
    print(f"| Initial Solution: {init_solution}")
    print(f"| The final score was: {score}")
    print("-------------------------------------------------------------")


# Algorithm 3
def algorithm3(file_path,init_solution):
    alg_name = "Algorithmo 3 :)"
    score = 0
    print_info(alg_name,file_path,init_solution,score)
    return 0

# Algorithm 2
def algorithm2(file_path,init_solution):
    alg_name = "Algorithmo 3 :)"
    score = 0
    print_info(alg_name,file_path,init_solution,score)
    return 0

# Algorithm 1
def algorithm1(file_path,init_solution):
    alg_name = "Algorithmo 1 :)"
    score = 0
    print_info(alg_name,file_path,init_solution,score)
    return 0

