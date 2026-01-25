#Definition of App class
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome to the Quizzler")
        self.geometry("500x500")

app = App()

app.mainloop()