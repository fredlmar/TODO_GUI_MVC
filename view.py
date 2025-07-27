# view.py

import tkinter as tk

class TaskView(tk.Frame):
    """
    View for the To-Do List GUI application.

    Provides the graphical interface and user input elements.
    """
    def __init__(self, master, controller):
        """
        Initialize the view and create all widgets.

        Args:
            master: The Tkinter root window.
            controller: The controller instance.
        """
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

        self.save_button = tk.Button(self, text="Save Tasks", command=self.controller.save_tasks)
        self.save_button.pack()

    def get_input(self):
        """
        Get the current text from the input field.

        Returns:
            str: The entered task text.
        """
        return self.task_entry.get()

    def clear_input(self):
        """
        Clear the input field.
        """
        self.task_entry.delete(0, tk.END)

    def update_tasks(self, tasks):
        """
        Update the listbox to show all current tasks.

        Args:
            tasks (list): The list of tasks to display.
        """
        self.tasks_listbox.delete(0, tk.END)
        for task in tasks:
            self.tasks_listbox.insert(tk.END, task)

    def get_selected_index(self):
        """
        Get the index of the currently selected task in the listbox.

        Returns:
            int or None: The index if a task is selected, otherwise None.
        """
        try:
            return self.tasks_listbox.curselection()[0]
        except IndexError:
            return None
