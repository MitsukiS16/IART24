import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
# Assuming 'algorithms' is a module you've written for handling the algorithmsimport algorithms as algo
import algorithms as algo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BookScannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Scanner Application")
        self.geometry("400x400")
        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Welcome to our application", font=("Arial", 16)).pack(pady=20)
        
        ttk.Button(self.main_frame, text="Book Scanning", command=self.book_scanning_menu).pack(pady=10)
        #ttk.Button(self.main_frame, text="See the best score for each library", command=self.best_score_menu).pack(pady=10)
        ttk.Button(self.main_frame, text="Exit", command=self.exit_application).pack(pady=10)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()

    def book_scanning_menu(self):
        self.clear_frame(self.main_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.book_scanning_frame, text="Book Scanning Menu", font=("Arial", 16)).pack(pady=20)

        file_options = ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]
        self.file_var = tk.StringVar()
        self.file_var.set(file_options[0])
        ttk.Label(self.book_scanning_frame, text="Please select an input file:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.file_var, *file_options)
        file_menu.pack(pady=5)

        ttk.Button(self.book_scanning_frame, text="Select Algorithm and Run", command=self.select_initial_sol).pack(pady=20)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)

    def select_initial_sol(self):
        self.clear_frame(self.book_scanning_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.book_scanning_frame, text="Book Scanning Menu", font=("Arial", 16)).pack(pady=20)
        init_sol_options = ["Random Solution","Trivial Solution","Greedy Solution"]
        self.init_sol_var = tk.StringVar()
        self.init_sol_var.set(init_sol_options[0])
        print("initial_solution" , self.init_sol_var.get())
        ttk.Label(self.book_scanning_frame, text="Please select the initial solution:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.init_sol_var, *init_sol_options)
        file_menu.pack(pady=5)
        ttk.Button(self.book_scanning_frame, text="Next", command=self.select_algorithm).pack(pady=20)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)

    def select_algorithm(self):
        self.clear_frame(self.book_scanning_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)
        
        selected_file = self.file_var.get()
        ttk.Label(self.book_scanning_frame, text="Book Scanning Menu", font=("Arial", 16)).pack(pady=20)
        algorithm_options = ["Simulated Annealing","Tabu Search","Genetic Algorithm"]
        self.sel_alg_var = tk.StringVar()
        self.sel_alg_var.set(algorithm_options[0])
        ttk.Label(self.book_scanning_frame, text="Please select the initial solution:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.sel_alg_var, *algorithm_options)
        file_menu.pack(pady=5)
        ttk.Button(self.book_scanning_frame, text="Next", command=self.run_algorithm).pack(pady=20)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)


    def run_algorithm(self):
        self.clear_frame(self.book_scanning_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)

    # Maps to link user selection to actual function
        algorithm_map = {
            "Simulated Annealing": (algo.get_sa_solution, "Simulated Annealing"),
            "Tabu Search": (algo.tabu_search, "Tabu Search"),
            "Genetic Algorithm": (algo.genetic_algorithm, "Genetic Algorithm")
        }

        initial_solution_map = {
            "Random Solution": algo.generate_random_solution, 
            # "Trivial Solution": algo.trivial_solution,  # Example addition
            # "Greedy Solution": algo.greedy_solution,   # Example addition
        }

        # Fetch the function based on user selection
        algorithm_func = algorithm_map.get(self.sel_alg_var.get())
        print("algorithm:", self.sel_alg_var.get())
    
        initial_solution = initial_solution_map.get(self.init_sol_var.get())
    
        self.selected_file_path = "../libraries/" + self.file_var.get() + ".txt"

        print("path:", self.selected_file_path)
        print("init", self.init_sol_var.get())
        print("algorithm:", self.sel_alg_var.get())
        
        if algorithm_func and initial_solution:
            try:
                best_solution , best_score, scores = algorithm_func[0](self.selected_file_path, initial_solution)

                # Display the result or further process it
        
                ttk.Label(self.book_scanning_frame, text=f"best solution: {best_solution}", font=("Arial", 16)).pack(pady=20)
                ttk.Label(self.book_scanning_frame, text=f"best_score: {best_score}", font=("Arial", 16)).pack(pady=20)
                ttk.Label(self.book_scanning_frame, text=f"scores:{scores}", font=("Arial", 16)).pack(pady=20)
            except Exception as e:
                ttk.Label(self.book_scanning_frame, text=f"Error: {str(e)}", font=("Arial", 16)).pack(pady=20)
        else:
            ttk.Label(self.book_scanning_frame, text="Invalid selection or error in execution", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)
        ttk.Button(self.book_scanning_frame, text="Exit", command=self.exit_application).pack(pady=10)

    def return_to_main_menu(self):
        self.clear_frame(self.book_scanning_frame)
        self.create_main_menu()

    def exit_application(self):
        self.quit()

if __name__ == "__main__":
    app = BookScannerGUI()
    app.mainloop()
