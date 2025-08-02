# controller.py


import tkinter as tk
from model import TaskModel
from view import TaskView
from tkinter import messagebox
import datetime

class TaskController:
    def mark_dirty(self):
        """
        Mark the application as having unsaved changes.
        """
        self._dirty = True

    def mark_clean(self):
        """
        Mark the application as having no unsaved changes.
        """
        self._dirty = False

    def is_dirty(self):
        """
        Return True if there are unsaved changes.
        """
        return getattr(self, '_dirty', False)

    def on_closing(self):
        """
        Ask to save changes if there are unsaved changes before closing.
        """
        if self.is_dirty():
            result = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Save before exiting?")
            if result is None:
                return  # Cancel close
            elif result:
                self.save_tasks()
        self.view.master.destroy()

    def set_task_done(self) -> None:
        """
        Toggle the 'done' status of the selected task. If setting to done, include the current date.
        """
        index = self.view.get_selected_index()
        if index is not None:
            tasks = self.model.get_tasks()
            if 0 <= index < len(tasks):
                task = tasks[index]
                if isinstance(task, tuple):
                    # Support (task_text, owner, done) or (task_text, owner, done, date)
                    if len(task) == 4:
                        task_text, owner, done, date_done = task
                    elif len(task) == 3:
                        task_text, owner, done = task
                        date_done = None
                    elif len(task) == 2:
                        task_text, owner = task
                        done = False
                        date_done = None
                    else:
                        return
                    # Toggle the done status
                    if not done:
                        # Set to done, add date
                        date_str = datetime.date.today().isoformat()
                        self.model.tasks[index] = (task_text, owner, True, date_str)
                    else:
                        # Set to not done, remove date
                        self.model.tasks[index] = (task_text, owner, False, None)
                    self.view.update_tasks(self.model.get_tasks(), selected_index=index)
                    self.mark_dirty()
        else:
            from tkinter import messagebox
            messagebox.showwarning("No selection", "Please select a task to toggle its done status.")

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
        self._dirty = False
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
                task = tasks[index]
                if isinstance(task, tuple):
                    task_text = task[0]
                else:
                    task_text = str(task)
                new_owner = self.view.owner_var.get()
                # Preserve done status if present
                if isinstance(task, tuple) and len(task) == 3:
                    _, _, done = task
                    self.model.tasks[index] = (task_text, new_owner, done)
                else:
                    self.model.tasks[index] = (task_text, new_owner)
                self.view.update_tasks(self.model.get_tasks(), selected_index=index)
                self.mark_dirty()
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
            self.mark_dirty()

    def delete_task(self) -> None:
        """
        Delete the selected task from the model and update the view.
        Shows a warning if no task is selected.
        """
        index = self.view.get_selected_index()
        if index is not None:
            self.model.delete_task(index)
            # Try to keep selection at the same index, or previous if last was deleted
            new_size = len(self.model.get_tasks())
            new_index = min(index, new_size - 1) if new_size > 0 else None
            self.view.update_tasks(self.model.get_tasks(), selected_index=new_index)
            self.mark_dirty()
        else:
            messagebox.showwarning("No selection", "Please select a task to delete.")

    def save_tasks(self) -> None:
        """
        Save all tasks to a file using the model.
        Shows a message box on success or error.
        """
        success = self.model.save_tasks()
        if success:
            # TODO: #11 change text in messagebox
            messagebox.showinfo("Tasks Saved!", "All tasks have been saved successfully.")
            self.mark_clean()
        else:
            messagebox.showerror("Save Failed", "Failed to save tasks.")
