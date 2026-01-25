#Definition of App class
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Welcome to the Quizzler")
        self.geometry("500x500")
        self.start_button = tk.Button(self, text="Start")
        self.quit_button = tk.Button(self, text="Quit")


app = App()

app.mainloop()