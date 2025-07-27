# controller.py

from model import TaskModel
from view import TaskView
from tkinter import messagebox

class TaskController:
    def __init__(self, root):
        self.model = TaskModel()
        self.view = TaskView(root, self)
        self.view.update_tasks(self.model.get_tasks())

    def add_task(self):
        task = self.view.get_input()
        self.model.add_task(task)
        self.view.update_tasks(self.model.get_tasks())
        self.view.clear_input()

    def delete_task(self):
        index = self.view.get_selected_index()
        if index is not None:
            self.model.delete_task(index)
            self.view.update_tasks(self.model.get_tasks())
        else:
            messagebox.showwarning("No selection", "Please select a task to delete.")
