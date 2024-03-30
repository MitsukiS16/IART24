import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import time
# Assuming 'algorithms' is a module you've written for handling the algorithmsimport algorithms as algo
import algorithms as algo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk

class BookScannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Scanner Application")
        self.geometry("300x300")
        #self.load_background_image('background_image.png')
        self.create_main_menu()
        #self.load_background_image('background_image.png')
        self.after(100, self.lift_main_frame)

    def load_background_image(self, image_path):
        bg_image = Image.open(image_path).resize((600, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(bg_image)

        # Add the background image to a label
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()  # Place the background label below other widgets in the same parent
        self.background_label.image = self.background_photo  # Keep a reference

    def lift_main_frame(self):
        self.main_frame.lift()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Welcome to our application", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.main_frame, text="Book Scanning", command=self.book_scanning_menu).pack(pady=10)
        ttk.Button(self.main_frame, text="See the best score for each library").pack(pady=10)
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
        ttk.Label(self.book_scanning_frame, text="Please select the initial solution:").pack(pady=5)
        file_menu = ttk.OptionMenu(self.book_scanning_frame, self.init_sol_var, *init_sol_options)
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
            "Genetic Algorithm": (algo.genetic_algorithm, "Genetic Algorithm"),
            "Hill Climbing Algorithm": (algo.hill_climbing_algorithm, "Hill Climbing Algorithm")
        }

        initial_solution_map = {
            "Random Solution": algo.generate_random_solution, 
            # "Trivial Solution": algo.trivial_solution, 
            # "Greedy Solution": algo.greedy_solution,  
        }

        # Fetch the function based on user selection
        algorithm_func = algorithm_map.get(self.sel_alg_var.get())
    
        initial_solution = initial_solution_map.get(self.init_sol_var.get())
    
        self.selected_file_path = "../input/" + self.file_var.get() + ".txt"

        print("path:", self.selected_file_path)
        print("init", self.init_sol_var.get())
        print("algorithm:", self.sel_alg_var.get())

        start_time = time.time()

        if algorithm_func and initial_solution:
            try:
                self.best_solution , self.best_score, self.scores = algorithm_func[0](self.selected_file_path, initial_solution)
                print("Best solution:", self.best_solution)
                print("Best score:", self.best_score)
                print("Scores:", self.scores)
                # Create a Text widget
                result_text = tk.Text(self.book_scanning_frame, height=10, width=50)
                result_text.pack(pady=20)

                # Configure tags for different text styles
                result_text.tag_configure("style", foreground="black", font=("Arial", 14))
                result_text.tag_configure("highlight", foreground="red", font=("Arial", 14))

                # Insert the results into the Text widget with the specified styles
                #result_text.insert(tk.END, "Best solution: ", "highlight")
                #result_text.insert(tk.END, f"{best_solution}\n", "style")
                result_text.insert(tk.END, "Best Score: ", "highlight")
                result_text.insert(tk.END, f"{self.scores}\n", "style")

                end_time = time.time() # End time
                elapsed_time = end_time - start_time 

                result_text.insert(tk.END, "Time taken: ", "highlight")
                result_text.insert(tk.END, f"{elapsed_time:.6f} seconds\n", "style")

            except Exception as e:
                ttk.Label(self.book_scanning_frame, text=f"Error: {str(e)}", font=("Arial", 16)).pack(pady=20)
        else:
            ttk.Label(self.book_scanning_frame, text="Invalid selection or error in execution", font=("Arial", 16)).pack(pady=20)
        button_frame = ttk.Frame(self.book_scanning_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="See Results", command=self.see_results).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="See Graph", command=self.display_graph).pack(side=tk.LEFT)   
        ttk.Button(self.book_scanning_frame, text="Return to Main Menu", command=self.return_to_main_menu).pack(pady=10)
        #ttk.Button(self.book_scanning_frame, text="Exit", command=self.exit_application).pack(pady=10)
        
    def display_graph(self):
        # Create a new figure and axes
        fig, ax = plt.subplots()

        # Generate x-coordinates for the bars
        x = range(len(self.best_solution))

        # Plot the scores from the best_solution list as a bar graph
        for i in range(len(self.best_solution[0])):
            ax.bar(x, [pt[i] for pt in self.best_solution])

        # Set labels for the x-axis, y-axis, and the title of the graph
        ax.set_xlabel("Instance")
        ax.set_ylabel("Score Value")
        ax.set_title("Score Variation per Instance")

        # Create a new Toplevel window
        graph_window = tk.Toplevel(self.book_scanning_frame)

        # Create a canvas and add the plot to it
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()

        # Add the canvas to the tkinter frame
        canvas.get_tk_widget().pack()

        
    def see_results(self):
        self.sol_output = "../output/" + self.file_var.get() + ".txt"
        os.system(f"code {self.sol_output}")

    def best_score_menu(self):
        self.clear_frame(self.main_frame)
        self.scores_frame = ttk.Frame(self.main_frame)
        self.scores_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('file', 'algorithm', 'score')
        self.scores_tree = ttk.Treeview(self.scores_frame, columns=columns, show='headings')
        for col in columns:
            self.scores_tree.heading(col, text=col.capitalize())
        self.scores_tree.pack(fill=tk.BOTH, expand=True)

        # Mock data
        scores = [
            ('a_example', 'Simulated Annealing', 95),
            ('b_read_on', 'Tabu Search', 88),
            # Add more scores as needed
        ]

        for score in scores:
            self.scores_tree.insert('', tk.END, values=score)

    def return_to_main_menu(self):
        self.clear_frame(self.book_scanning_frame)
        self.create_main_menu()

    def exit_application(self):
        self.quit()

if __name__ == "__main__":
    app = BookScannerGUI()
    app.mainloop()
