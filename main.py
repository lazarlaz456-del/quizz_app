#Definition of App class
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import requests as rq
import html
import sqlite3
from datetime import datetime

base_dir_path = os.path.dirname(os.path.abspath(__file__))

class App(tk.Tk):
    #Initialize the window
    def __init__(self):
        super().__init__()
        self.title("Welcome to the Quizzler")
        self.config(padx=3, pady=3)

        #Initialize the canvas
        self.canvas = tk.Canvas(self, bg="#D3D3D3", height=500, width=500)
        self.canvas.grid(row=0, column=0, rowspan=6, columnspan=5, sticky="nsew")

        #Initialize the start button
        self.start_button = tk.Button(self, text="Start", font=("Times New Roman", 18, "italic"), bg="#45A049", fg="white",
                                    relief="flat", activebackground="#43A047", activeforeground="black", command=self.start_or_restart_game)
        self.start_button.grid(row=0, column=1, padx=10, pady=10)

        #Initialize the quit button
        self.quit_button = tk.Button(self, text="Quit", font=("Times New Roman", 18, "italic"), bg="black", fg="white",
                                    relief="flat", activebackground="#333333", activeforeground="white", command=self.quit_game)
        self.quit_button.grid(row=0, column=3, padx=10, pady=10)

        #Initialize text area where questions will be displayed
        self.text_area = tk.Text(self, height=10, wrap="word")
        self.text_area.grid(row=1, column=1, padx=10, pady=10, columnspan=3, rowspan=3, sticky="nsew")

        #Initialize True button
        img_path_true = os.path.join(base_dir_path, "true.png")
        self.true_img = tk.PhotoImage(file=img_path_true)
        self.true_button = tk.Button(self, image=self.true_img, command=self.true_button_choice)
        self.true_button.grid(row=4, column=1, padx=10, pady=10)

        #Initialize False button
        img_path_false = os.path.join(base_dir_path, "false.png")
        self.false_img = tk.PhotoImage(file=img_path_false)
        self.false_button = tk.Button(self, image=self.false_img, command=self.false_button_choice)
        self.false_button.grid(row=4, column=3, padx=10, pady=10)

        #Initialize score label
        self.score = 0
        self.score_label = tk.Label(self, text=f"SCORE\n{self.score}/10", anchor="center", font=("Times New Roman", 20, "bold"), bg="#D3D3D3")
        self.score_label.grid(row=4, column=2, padx=10, pady=10)

        #Initialize question number label
        self.question_label = tk.Label(self, text="", anchor="center", font=("Times New Roman", 20, "bold"), bg="#D3D3D3")
        self.question_label.grid(row=0, column=2, padx=10, pady=10)

        #Update the close button of the window
        self.protocol("WM_DELETE_WINDOW", self.quit_game)
        
        #Initialize Score button
        self.show_results_button = tk.Button(self, text="Show results", font=("Times New Roman", 18, "italic"), bg="#26C6DA", fg="white", relief="flat",
                                             activebackground="black", activeforeground="#1FA3B4", command=self.display_results)
        self.show_results_button.grid(row=5, column=2, padx=10, pady=10)

        self.question_key = 1

    #Function to start/restart game - used with the start button
    def start_or_restart_game(self):

        if self.question_key == 1:
            self.get_question_bank()
        else:

            if 1 < self.question_key <= 10:
                restart_game = messagebox.askyesno("Restart game?", "You have pressed start while a quiz is already running, do you wish to restart game?")

                if restart_game:
                    self.save_game()
                    self.score = 0
                    self.question_key = 1
                    self.get_question_bank()

            else:
                self.score = 0
                self.question_key = 1
                self.get_question_bank()

    #Function to get the question bank using API
    def get_question_bank(self):
        url = "https://opentdb.com/api.php?amount=10&type=boolean"
        response = rq.get(url)
        data = response.json()

        questions_raw = data["results"]
        questions_clean = dict()

        counter_key = 1
        for question in questions_raw:
            question_string = html.unescape(question["question"])
            question_answer = question["correct_answer"]
            question_category = question["category"]
            questions_clean[counter_key] = {"question": question_string, "category": question_category, "answer": question_answer}
            counter_key += 1
        
        self.question_bank = questions_clean
        self.current_question = self.question_bank[self.question_key]["question"]

        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", self.current_question)

        self.question_label.config(text=f"Question {self.question_key}")
        self.score_label.config(text=f"SCORE\n{self.score}/10")

        self.true_button.config(state="normal")
        self.false_button.config(state="normal")

    # Function to get the choice and update score if user picked True
    def true_button_choice(self):
        self.choice = "True"
        self.get_result_next_question()

    #Same for False
    def false_button_choice(self):
        self.choice = "False"
        self.get_result_next_question()

    #Function to iterate over the question bank and select the next question
    def get_result_next_question(self):
        if self.choice == self.question_bank[self.question_key]["answer"]:
            text_to_write = "Bravo! Your answer is correct!"
            self.score += 1
            self.score_label.config(text=f"SCORE\n{self.score}/10")
        else:
            text_to_write = "Not Quite! Your answer is wrong!"
        
        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", text_to_write)

        self.after(1500, self.next_question)

    #Function to switch to next question and to stop the game once all questions have been answered
    def next_question(self):
        try:
            self.question_key += 1
            self.current_question = self.question_bank[self.question_key]["question"]
        except KeyError:
            text_to_write = f"You have answered all of the questions in this quiz! You scored {self.score} points\nIf You wish to restart the quiz press Start"
            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", text_to_write)
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.save_game()
        else:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", self.current_question)
            self.question_label.config(text=f"Question {self.question_key}")
    
    def quit_game(self):
        if self.question_key < 11:
            quit_during_game = messagebox.askyesno("Quit during game?", "Are you sure you want to quit? The round is still going")
            
            if quit_during_game:
                self.save_game()
                self.destroy()

        else:
            quit_after_game = messagebox.askyesno("Quit game?", "Are you sure you want to quit?")
            
            if quit_after_game:
                self.destroy()
        
    def save_game(self):
        conn = sqlite3.connect("quiz_results.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS results (game_id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER, date TEXT, timestamp TEXT, status TEXT)""")
        
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        timestamp = now.strftime("%H:%M:%S")

        if self.question_key < 11:
            status = "Unfinished"
        else:
            status = "Finished"

        messagebox.showinfo("Info message", "Saving game...")
        cursor.execute("""INSERT INTO results (score, date, timestamp, status) VALUES (?, ?, ?, ?)""", (self.score, date, timestamp, status))

        conn.commit()
        conn.close()

    def display_results(self):
        if not os.path.exists(os.path.join(base_dir_path, "quiz_results.db")):
            messagebox.showinfo("Info message", "No results to display, start your first game ;)")
        else:
            
            results_window = tk.Toplevel(self)
            results_window.title("Game results")
            results_window.geometry("500x300")
            results_window.configure(bg="#D3D3D3")

            columns = ("game_id", "score", "date", "timestamp", "status")

            tree = ttk.Treeview(results_window, columns=columns, show="headings", height=15)

            tree.heading("game_id", text="Game ID")
            tree.heading("score", text="Score")
            tree.heading("date", text="Date")
            tree.heading("timestamp", text="Time")
            tree.heading("status", text="Status")

            tree.column("game_id", width=80, anchor="center")
            tree.column("score", width=60, anchor="center")
            tree.column("date", width=120, anchor="center")
            tree.column("timestamp", width=120, anchor="center")
            tree.column("status", width=100, anchor="center")

            scrollbar = ttk.Scrollbar(
                results_window,
                orient="vertical",
                command=tree.yview
            )
            tree.configure(yscrollcommand=scrollbar.set)
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            conn = sqlite3.connect("quiz_results.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM results ORDER BY game_id DESC")
            rows = cursor.fetchall()

            conn.close()

            for row in rows:
                tree.insert("", tk.END, values=row)

app = App()

app.mainloop()