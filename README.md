# IART24

## Project Description

This is a Python application deesigend to given a description of libraries and books available, plan which books to scan from which library to maximize the total score of all scanned books, taking into account that each library needs to be signed up before it can ship books

`Note: Your score is the sum of the scores of all books that are scanned within D days. Note that if the same book is shipped from multiple libraries (as books 2 and 3 are in the gure below), the solution will be accepted but the score for the book will be awarded only once.`

## Installation and Usage

To  run our application, follow these simple steps:
1. Open a terminal window
2. Navigate to the src folder using the cd command: `cd src`
3. Execute the following command to compile and run the program: `python main.py`

Please be aware that if you have multiple versions of Python installed, you may need to specify the version you want to use. 

**Note**: If the program's output exceeds the terminal windows's size, you can use the following command to view the entire output and save it to a file for future reference: `python main.py | tee output.txt`


## Project Scruture

...

## Collaboration

- Clarisse Maria Teixeira de Carvalho, up202008444
- Válter Ochôa de Spínola Catanho Castro, up
- Sandra Patricia Linhares Miranda, up

## Algorithms

Here's a summary of the categories and some of the algorithms listed under each:

[ ] Swarm Intelligence Algorithms:

- [ ] Particle Swarm Optimization (PSO)
- [ ] Ant Colony Optimization (ACO)
- [ ] Bee Colony Optimization (BCO)
- [ ] Firefly Algorithm (FA)

[ ] Simulated Annealing (SA) and its variants:

- [ ] Quantum Annealing
- [ ] Fast Simulated Annealing
- [ ] Parallel Tempering

[ ] Tabu Search (TS) and its variants:

- [ ] Reactive Tabu Search
- [ ] Guided Tabu Search
- [ ] Iterated Tabu Search

[ ] Local Search Algorithms:

- [ ] Hill Climbing
- [ ] Iterated Local Search (ILS)
- [ ] Variable Neighborhood Search (VNS)

[ ] Memetic Algorithms (MA):

- [ ] Hybridization of genetic algorithms with local search methods

[ ] Estimation of Distribution Algorithms (EDA):

- [ ] Bayesian Optimization Algorithm (BOA)
- [ ] Compact Genetic Algorithm (CGA)
- [ ] Univariate Marginal Distribution Algorithm (UMDA)

[ ] Hybrid Algorithms:

- [ ] Combining multiple metaheuristics or metaheuristics with exact methods to leverage their complementary strengths

## Restricitions

### Library signup

Each library has to go through a signup process before books from that library can be shipped. Only one library at a time can be going through this process (because it involves lots of planning and on-site visits at the library by logistics expes): the signup process for a library can sta only when no other signup processes are running. The libraries can be signed up in any order. Books in a library can be scanned as soon as the signup process for that library completes (that is, on the rst day immediately aer the signup process, see the gure below). Books can be scanned in parallel from multiple libraries.

### Scanning

All books are scanned in the scanning facility. The entire process of sending the books, scanning them, and returning them to the library happens in one day (note that each library has a maximum number of books that can be scanned from this library per day). The scanning facility is big and can scan any number of books per day.

## Deadline

CheckPoint:
[ ] Presentation (max.5 slides), in pdf format

Final:
[ ] Presentation (max.10 slides), in pdf format

### Scoring
