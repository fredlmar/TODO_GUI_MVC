# main.py

import tkinter as tk
from controller import TaskController

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskController(root)
    root.mainloop()
