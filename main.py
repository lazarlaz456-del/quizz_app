#Definition of App class
import tkinter as tk
import os
import requests as rq
import html
import time

base_dir_path = os.path.dirname(os.path.abspath(__file__))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to the Quizzler")
        self.config(padx=3, pady=3)

        self.canvas = tk.Canvas(self, bg="#D3D3D3", height=500, width=500)
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")

        self.start_button = tk.Button(self, text="Start", font=("Times New Roman", 18, "italic"), bg="#45A049", fg="white",
                                    relief="flat", activebackground="#43A047", activeforeground="black", command=self.get_question_bank)
        self.start_button.grid(row=0, column=1, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Quit", font=("Times New Roman", 18, "italic"), bg="black", fg="white",
                                    relief="flat", activebackground="#333333", activeforeground="white")
        self.quit_button.grid(row=0, column=3, padx=10, pady=10)

        self.text_area = tk.Text(self, height=10, wrap="word")
        self.text_area.grid(row=1, column=1, padx=10, pady=10, columnspan=3, rowspan=3, sticky="nsew")

        img_path_true = os.path.join(base_dir_path, "true.png")
        self.true_img = tk.PhotoImage(file=img_path_true)
        self.true_button = tk.Button(self, image=self.true_img)
        self.true_button.grid(row=4, column=1, padx=10, pady=10)

        img_path_false = os.path.join(base_dir_path, "false.png")
        self.false_img = tk.PhotoImage(file=img_path_false)
        self.false_button = tk.Button(self, image=self.false_img)
        self.false_button.grid(row=4, column=3, padx=10, pady=10)

        self.score = 0
        self.score_label = tk.Label(self, text=f"SCORE\n{self.score}/10", anchor="center", font=("Times New Roman", 20, "bold"), bg="#D3D3D3")
        self.score_label.grid(row=4, column=2, padx=10, pady=10)

    def get_question_bank(self):
        url = "https://opentdb.com/api.php?amount=20&type=boolean"
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
        self.current_question = self.question_bank[1]

        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", self.current_question["question"])

    def true_button_choice(self):
        self.choice = "True"

    def false_button_choice(self):
        self.choice = "False"

    def get_result_next_question(self):
        if self.choice == self.question_bank["answer"]:
            pass









app = App()

app.mainloop()