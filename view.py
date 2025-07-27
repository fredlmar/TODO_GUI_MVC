# view.py

import tkinter as tk

class TaskView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.master.title("To-Do List GUI")
        self.pack()

        self.task_entry = tk.Entry(self, width=40)
        self.task_entry.pack(pady=5)

        self.add_button = tk.Button(self, text="Add Task", command=self.controller.add_task)
        self.add_button.pack()

        self.tasks_listbox = tk.Listbox(self, width=50)
        self.tasks_listbox.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Selected Task", command=self.controller.delete_task)
        self.delete_button.pack()

    def get_input(self):
        return self.task_entry.get()

    def clear_input(self):
        self.task_entry.delete(0, tk.END)

    def update_tasks(self, tasks):
        self.tasks_listbox.delete(0, tk.END)
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task)

    def get_selected_index(self):
        try:
            return self.tasks_listbox.curselection()[0]
        except IndexError:
            return None
