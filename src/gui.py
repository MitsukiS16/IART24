import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import time
import generators as gen
import algorithms as algo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
from tabulate import tabulate
import csv

class BookScannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Scanner Application")
        self.geometry("300x300")
        self.create_main_menu()
        self.after(100, self.lift_main_frame)

    def lift_main_frame(self):
        self.main_frame.lift()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Welcome to our application", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.main_frame, text="Book Scanning", command=self.book_scanning_menu).pack(pady=10)
        ttk.Button(self.main_frame, text="See the best score for each library", command=self.best_score_menu).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.exit_application).pack(pady=10)
       
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
        ttk.Label(self.book_scanning_frame, text="Please select an input file:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.file_var, "Please select an input file", *file_options)
        file_menu.pack(pady=5)

        ttk.Button(self.book_scanning_frame, text="Select Algorithm and Run", command=self.select_initial_sol).pack(pady=20)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)

    def select_initial_sol(self):

        self.clear_frame(self.book_scanning_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.book_scanning_frame, text="Book Scanning Menu", font=("Arial", 16)).pack(pady=20)
        init_sol_options = ["Random Solution","Trivial Solution"]
        self.init_sol_var = tk.StringVar()
        ttk.Label(self.book_scanning_frame, text="Please select the initial solution:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.init_sol_var, "Please select an initial solution", *init_sol_options)
        file_menu.pack(pady=5)
        ttk.Button(self.book_scanning_frame, text="Next", command=self.select_algorithm).pack(pady=20)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)

    def select_algorithm(self):
        
        self.clear_frame(self.book_scanning_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)
        #selected_file = self.file_var.get()
        ttk.Label(self.book_scanning_frame, text="Book Scanning Menu", font=("Arial", 16)).pack(pady=20)
        algorithm_options = ["Simulated Annealing","Tabu Search","Genetic Algorithm","Hill Climbing Algorithm"]
        self.sel_alg_var = tk.StringVar()
        ttk.Label(self.book_scanning_frame, text="Please select the initial solution:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.sel_alg_var, "Please select an algorithm", *algorithm_options)
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
            "Genetic Algorithm": (algo.genetic_algorithm, "Genetic Algorithm"),
            "Hill Climbing Algorithm": (algo.hill_climbing_algorithm, "Hill Climbing Algorithm")
        }

        initial_solution_map = {
            "Random Solution": gen.generate_random_solution, 
            "Trivial Solution": gen.generate_trivial_solution 
        }

        # Fetch the function based on user selection
        algorithm_func = algorithm_map.get(self.sel_alg_var.get())
    
        initial_solution = initial_solution_map.get(self.init_sol_var.get())
    
        self.selected_file_path = "../input/" + self.file_var.get() + ".txt"

        #print("path:", self.selected_file_path)
        #print("init", self.init_sol_var.get())
        #print("algorithm:", self.sel_alg_var.get())



        start_time = time.time()

        if algorithm_func and initial_solution:
            try:
                self.best_solution , self.best_score, self.scores = algorithm_func[0](self.selected_file_path, initial_solution)
                xscrollbar = tk.Scrollbar(self.book_scanning_frame, orient=tk.HORIZONTAL)
                yscrollbar = tk.Scrollbar(self.book_scanning_frame, orient=tk.VERTICAL)
       
                # Create a Text widget
                result_text = tk.Text(self.book_scanning_frame, height=10, width=50, bg="lightgrey")
                result_text.pack(pady=20)

                result_text.tag_configure("style", foreground="black", font=("Arial", 14))
                result_text.tag_configure("highlight", foreground="red", font=("Arial", 14))
                result_text.insert(tk.END, "Algorithm : ", "highlight")
                result_text.insert(tk.END, f"{algorithm_func[1]}\n", "style")
                result_text.insert(tk.END, "Best Score: ", "highlight")
                if isinstance(self.scores, list):
                    max_score = max(self.scores)
                else:
                    max_score = self.scores
                result_text.insert(tk.END, f"{max_score}\n", "style")
                end_time = time.time() # End time
                elapsed_time = end_time - start_time 

                result_text.insert(tk.END, "Time taken: ", "highlight")
                result_text.insert(tk.END, f"{elapsed_time:.6f} seconds\n", "style")

                xscrollbar.config(command=result_text.xview)
                yscrollbar.config(command=result_text.yview)
                xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
                yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                # Set the window size to the size of its contents
                self.geometry('{}x{}'.format(result_text.winfo_reqwidth(), result_text.winfo_reqheight()))

            except Exception as e:
                ttk.Label(self.book_scanning_frame, text=f"Error: {str(e)}", font=("Arial", 16)).pack(pady=20)
        else:
            ttk.Label(self.book_scanning_frame, text="Invalid selection or error in execution", font=("Arial", 16)).pack(pady=20)
        button_frame = ttk.Frame(self.book_scanning_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="See Results", command=self.see_results).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="See Graph", command=self.display_graph).pack(side=tk.LEFT)
        ttk.Button(self.book_scanning_frame, text="Signup Process", command=self.signup_process).pack(pady=10)
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)
        
    def display_graph(self):
        # Create a new figure and axes
        fig, ax = plt.subplots()

        if self.sel_alg_var.get() == "Hill Climbing Algorithm":
            x = [0]
            ax.bar(x, [self.scores])
        else:
            x = range(len(self.scores))
            ax.bar(x, self.scores, edgecolor='black') 

        # Set labels for the x-axis, y-axis, and the title of the graph
        ax.set_xlabel("Instance")
        ax.set_ylabel("Score Value")
        ax.set_title("Score Variation per Instance")
        # Create a new Toplevel window
        graph_window = tk.Toplevel(self.book_scanning_frame)

        # Create a canvas and add the plot to it
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        
    def see_results(self):
        self.sol_output = "../output/" + self.file_var.get() + ".txt"
        os.system(f"code {self.sol_output}")

    def best_score_menu(self):
        self.clear_frame(self.main_frame)
        self.book_scanning_frame = ttk.Frame(self)
        self.book_scanning_frame.pack(fill=tk.BOTH, expand=True)

        # Get the content of the best score
        content = self.get_content_best_score()
        # Create a Scrollbar and a Text widget
        xscrollbar = tk.Scrollbar(self.book_scanning_frame, orient=tk.HORIZONTAL)
        yscrollbar = tk.Scrollbar(self.book_scanning_frame, orient=tk.VERTICAL)
        # Create a Text widget
        text = tk.Text(self.book_scanning_frame, wrap=tk.NONE, height=25, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        text.insert(tk.END, content)
        text.grid(row=0, column=0, sticky='nsew')
        
        button = ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu)
        button.grid(row=1, column=0, pady=10)
        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)
        xscrollbar.grid(row=2, column=0, sticky='ew')
        yscrollbar.grid(row=0, column=1, sticky='ns', rowspan=2)

        self.book_scanning_frame.grid_columnconfigure(0, weight=1)
        self.book_scanning_frame.grid_rowconfigure(0, weight=1)

        # Set the window size to the size of its contents
        self.geometry('{}x{}'.format(text.winfo_reqwidth(), text.winfo_reqheight()))

    def get_content_best_score(self):
        with open('best_score.txt', 'r') as f:
            lines = f.readlines()
        # Initialize table headers and rows
        headers = ['File', 'Initial Solution', 'Algorithm', 'Score', 'Time (sec)']
        rows = []
        lines = lines[1:]
        # Parse each line and extract relevant information
        for line in lines:
            file_name, initial_solution, algorithm, score, time = line.strip().split(',')
            rows.append([file_name.strip(), initial_solution.strip(), algorithm.strip(), int(score), float(time)])
        # Generate the table
        table = tabulate(rows, headers=headers)
        # Replace spaces with non-breaking spaces
        table = table.replace(' ', '\u00A0')
        return table

    def return_to_main_menu(self):
        self.clear_frame(self.book_scanning_frame)
        self.create_main_menu()

    def exit_application(self):
        self.quit()

    def signup_process(self):
        # Create the graph

        books_per_day = gen.books_per_day
        plt.figure(figsize=(10, 6))
        days = range(len(books_per_day))
        plt.barh(days, books_per_day,color='skyblue')
        plt.title('Library Signup Process')
        plt.xlabel('Books per day')
        plt.ylabel('Days')
        plt.show() 


if __name__ == "__main__":
    app = BookScannerGUI()
    app.mainloop()