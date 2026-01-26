#Definition of App class
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to the Quizzler")
        self.config(padx=3, pady=3)

        self.canvas = tk.Canvas(self, bg="#D3D3D3", height=500, width=500)
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")

        self.start_button = tk.Button(self, text="Start", font=("Times New Roman", 18, "italic"), bg="#45A049", fg="white",
                                    relief="flat", activebackground="#43A047", activeforeground="black")
        self.start_button.grid(row=0, column=1, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Quit", font=("Times New Roman", 18, "italic"), bg="black", fg="white",
                                    relief="flat", activebackground="#333333", activeforeground="white")
        self.quit_button.grid(row=0, column=3, padx=10, pady=10)

        self.text_area = tk.Text(self, height=10, wrap="word")
        self.text_area.grid(row=1, column=1, padx=10, pady=10, columnspan=3, rowspan=3, sticky="nsew")
        


app = App()

app.mainloop()