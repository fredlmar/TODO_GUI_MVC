# controller.py

import tkinter as tk
from model import TaskModel
from view import TaskView
from tkinter import messagebox

class TaskController:

    def toggle_owner_filter(self) -> None:
        """
        Toggle the filter for showing only tasks of the selected owner.
        """
        if self.view.filter_var.get():
            owner = self.view.owner_var.get()
            self.view.update_tasks(self.model.get_tasks(), filter_owner=owner)
        else:
            self.view.update_tasks(self.model.get_tasks())

    def filter_tasks_by_owner(self) -> None:
        """
        Filter and show only tasks of the selected owner in the view.
        """
        owner = self.view.owner_var.get()
        self.view.update_tasks(self.model.get_tasks(), filter_owner=owner)
    """
    Controller for the To-Do List GUI application.

    Connects the model and view, and handles user interactions.
    """
    def __init__(self, root: 'tk.Tk') -> None:
        """
        Initialize the controller, load tasks from file, and set up the view.

        Args:
            root: The Tkinter root window.
        """
        self.model = TaskModel()
        self.model.load_tasks()
        self.view = TaskView(root, self)
        self.view.update_tasks(self.model.get_tasks())

    def modify_owner(self) -> None:
        """
        Modify the owner of the selected task to the currently selected owner in the dropdown.
        """
        index = self.view.get_selected_index()
        if index is not None:
            tasks = self.model.get_tasks()
            if 0 <= index < len(tasks):
                task_text, _ = tasks[index] if isinstance(tasks[index], tuple) and len(tasks[index]) == 2 else (str(tasks[index]), "")
                new_owner = self.view.owner_var.get()
                self.model.tasks[index] = (task_text, new_owner)
                self.view.update_tasks(self.model.get_tasks())
        else:
            from tkinter import messagebox
            messagebox.showwarning("No selection", "Please select a task to change its owner.")
    def add_task(self) -> None:
        """
        Add a new task from the view input to the model and update the view.
        """
        task_text, owner = self.view.get_input()
        if task_text:
            self.model.add_task((task_text, owner))
            self.view.update_tasks(self.model.get_tasks())
            self.view.clear_input()

    def delete_task(self) -> None:
        """
        Delete the selected task from the model and update the view.
        Shows a warning if no task is selected.
        """
        index = self.view.get_selected_index()
        if index is not None:
            self.model.delete_task(index)
            self.view.update_tasks(self.model.get_tasks())
        else:
            messagebox.showwarning("No selection", "Please select a task to delete.")

    def save_tasks(self) -> None:
        """
        Save all tasks to a file using the model.
        Shows a message box on success or error.
        """
        success = self.model.save_tasks()
        if success:
            messagebox.showinfo("Tasks Saved", "All tasks have been saved successfully.")
        else:
            messagebox.showerror("Save Failed", "Failed to save tasks.")
