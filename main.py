# main.py

import tkinter as tk
from controller import TaskController

def main():
    root = tk.Tk()
    app = TaskController(root)
    # Set up window close protocol to check for unsaved changes
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

