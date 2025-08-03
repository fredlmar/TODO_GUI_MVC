# controller.py


import tkinter as tk
from model import TaskModel
from view import TaskView
from tkinter import messagebox
from datetime import datetime

class TaskController:
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
        self.view.owner_options = self.model.owners.copy()
        self.view.set_owner_dropdown(self.model.owners[0] if self.model.owners else "No Owner")
        self.view.update_tasks(self.model.get_tasks())
        self.unsaved_changes = False


    def on_closing(self):
        """
        Ask to save changes if there are unsaved changes before closing.
        """
        if self.unsaved_changes:
            result = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Save before exiting?")
            if result is None:
                return  # Cancel close
            elif result:
                self.save_tasks()
        self._cleanup()
        self.view.master.destroy()

    def _cleanup(self):
        """
        Perform any additional cleanup before closing the application.
        """
        # Remove trace callbacks to prevent memory leaks
        if hasattr(self.view, 'owner_var') and self.view.owner_var:
            try:
                # Get all trace callbacks and remove them
                for trace_id in self.view.owner_var.trace_info():
                    self.view.owner_var.trace_remove('write', trace_id[0])
            except (AttributeError, tk.TclError):
                # Ignore errors if traces are already removed or widget is destroyed
                pass
        
        # Clear model data to help with garbage collection
        if hasattr(self, 'model') and self.model:
            self.model.tasks.clear()
            self.model.owners.clear()

    def set_task_done(self):
        selected = self.view.tasks_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        tasks = self.model.get_tasks()
        if 0 <= index < len(tasks):
            task_text, owner, done, date_done = tasks[index]
            if done:
                # Mark as not done
                tasks[index] = (task_text, owner, False, None)
            else:
                # Mark as done
                date_done = datetime.now().strftime("%Y-%m-%d %H:%M")
                tasks[index] = (task_text, owner, True, date_done)
            self.view.update_tasks(tasks, selected_index=index)
            self.unsaved_changes = True

    def toggle_owner_filter(self) -> None:
        """
        Toggle the filter for showing only tasks of the selected owner.
        """
        filter_enabled = self.view.filter_var.get()
        owner = self.view.owner_var.get() if filter_enabled else None
        self.view.update_tasks(self.model.get_tasks(), filter_owner=owner)

    def filter_tasks_by_owner(self) -> None:
        """
        Filter and show only tasks of the selected owner in the view.
        """
        owner = self.view.owner_var.get()
        self.view.update_tasks(self.model.get_tasks(), filter_owner=owner)
    def add_task(self) -> None:
        """
        Add a new task from the view input to the model and update the view.
        """
        task_text, owner = self.view.get_input()
        if not task_text or not owner:
            messagebox.showwarning("Input Error", "Task and owner must be specified.")
            return
        self.model.add_task((task_text, owner))
        self.view.update_tasks(self.model.get_tasks())
        self.view.clear_input()
        self.unsaved_changes = True

    def delete_task(self) -> None:
        """
        Delete the selected task from the model and update the view.
        Shows a warning if no task is selected.
        """
        selected = self.view.tasks_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        if self.model.delete_task(index):
            self.view.update_tasks(self.model.get_tasks())
            self.unsaved_changes = True

    def save_tasks(self) -> None:
        """
        Save all tasks to a file using the model.
        Shows a message box on success or error.
        """
        try:
            self.model.save_tasks()
            self.unsaved_changes = False
            messagebox.showinfo("Saved", "Tasks and owners saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def add_owner(self):
        new_owner = self.view.new_owner_entry.get().strip()
        if not new_owner:
            messagebox.showwarning("Input Error", "Owner name cannot be empty.")
            return
        if new_owner in self.model.owners:
            messagebox.showinfo("Info", "Owner already exists.")
            return
        try:
            self.model.add_owner(new_owner)
            self.view.owner_options = self.model.owners
            self.view.owner_var.set(new_owner)
            self.view.new_owner_entry.delete(0, tk.END)
            self.unsaved_changes = True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add owner: {e}")

    def modify_owner(self) -> None:
        """
        Modify the owner of the selected task to the currently selected owner in the dropdown.
        """
        selected = self.view.tasks_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        new_owner = self.view.owner_var.get()
        tasks = self.model.get_tasks()
        if 0 <= index < len(tasks):
            task_text, _, done, date_done = tasks[index]
            tasks[index] = (task_text, new_owner, done, date_done)
            self.view.update_tasks(tasks, selected_index=index)
            self.unsaved_changes = True
