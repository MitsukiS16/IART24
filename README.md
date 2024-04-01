# IART24

## Project Description

This is a Python application designed to given a description of libraries and books available, plan which books to scan from which library to maximize the total score of all scanned books, taking into account that each library needs to be signed up before it can ship books

`Note: Your score is the sum of the scores of all books that are scanned within D days. Note that if the same book is shipped from multiple libraries, the solution will be accepted but the score for the book will be awarded only once.`

## Installation and Usage

Additionally library: numpy, tabulate, matplotlib, concurrent.futures, hashlib, collections, math , random, copy, sys, os, tkinter

To run our application, follow these simple steps:

1. Open a terminal window
2. Navigate to the src folder using the cd command: `cd src`
3. Execute the following command to compile and run the program: `python main.py`

`Note`: If you want to run the application with a graphical interface, you should use the following command: `python gui.py`

Please be aware that if you have multiple versions of Python installed, you may need to specify the version you want to use.

**Note**: If the program's output exceeds the terminal windows's size, you can use the following command to view the entire output and save it to a file for future reference: `python main.py | tee output.txt`

## Project Scruture

1. Main Menu: Select input file 
2. SubMenu: Select initial Solution
- Random
- Trivial
3. SubMenu: Select the algorithm 
- Simulated Annealing
- Tabu Search
- Genetic Algorithm
- Hill Climbing Algorithm
4. Show graph


## Collaboration

- Clarisse Maria Teixeira de Carvalho, up202008444
- Válter Ochôa de Spínola Catanho Castro, up201706546
- Sandra Patricia Linhares Miranda, up202007675

## Algorithms

Initial Solutions:

- Random Solution
- Trivial Solution
- Greedy Constrution

Algorithms Implemented:

- [Metaheuristic Methods] Genetic Algorithm
- [Metaheuristic Methods] Simulated Annealing
- [Metaheuristic Methods] Tabu Search
- [Metaheuristic Methods] Hill Climbing Algorithm

## Restricitions

### Library signup

Each library has to go through a signup process before books from that library can be shipped. Only one library at a time can be going through this process (because it involves lots of planning and on-site visits at the library by logistics expes): the signup process for a library can sta only when no other signup processes are running. The libraries can be signed up in any order. Books in a library can be scanned as soon as the signup process for that library completes (that is, on the rst day immediately aer the signup process, see the gure below). Books can be scanned in parallel from multiple libraries.

### Scanning

All books are scanned in the scanning facility. The entire process of sending the books, scanning them, and returning them to the library happens in one day (note that each library has a maximum number of books that can be scanned from this library per day). The scanning facility is big and can scan any number of books per day.


### Results

## Results

| File  | Score |
| ------------- | ------------- |
| a_example ([input](input/a_example.txt) \| [output](output/a_example.out)) | 21 |
| b_read_on ([input](input/b_read_on.txt) \| [output](output/b_read_on.out)) | 0 |
| c_incunabula ([input](input/c_incunabula.txt) \| [output](output/c_incunabula.out)) | 0 |
| d_tough_choices ([input](input/d_tough_choices.txt) \| [output](output/d_tough_choices.out)) | 4,354,090 |
| e_so_many_books ([input](input/e_so_many_books.txt) \| [output](output/e_so_many_books.out)) | 0 |
| f_libraries_of_the_world ([input](input/f_libraries_of_the_world.txt) \| [output](output/f_libraries_of_the_world.out)) | 870870 |
| **Total** | **0** |
