# model.py
import os

class TaskModel:
    """
    Model for managing the list of tasks and file operations.

    Stores tasks in memory and provides methods to add, delete, save, and load tasks.
    """
    def __init__(self, filename="tasks.txt"):
        """
        Initialize the TaskModel with an empty task list.
        """
        self.filename = filename
        self.tasks = []
        self.owners = []
        self.load_tasks()

    def add_task(self, task):
        """
        Add a new task to the list.

        Args:
            task (tuple): The task to add, as (task_text, owner), (task_text, owner, done), or (task_text, owner, done, date_done).
        """
        if task and isinstance(task, tuple):
            if len(task) == 2:
                task_text, owner = task
                self.tasks.append((task_text, owner, False, None))
            elif len(task) == 3:
                task_text, owner, done = task
                self.tasks.append((task_text, owner, done, None))
            elif len(task) == 4:
                self.tasks.append(task)

    def get_tasks(self):
        """
        Get the current list of tasks.

        Returns:
            list: The list of tasks.
        """
        return self.tasks

    def delete_task(self, index):
        """
        Delete a task by its index.

        Args:
            index (int): The index of the task to delete.

        Returns:
            bool: True if the task was deleted, False otherwise.
        """
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False

    def save_tasks(self):
        """
        Save all tasks to a text file.
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("OWNERS:" + ",".join(self.owners) + "\n")
            for task in self.tasks:
                task_text, owner, done, date_done = task
                date_done_str = date_done if date_done else ""
                f.write(f"{task_text}|{owner}|{done}|{date_done_str}\n")

    def load_tasks(self):
        """
        Load tasks from a text file.
        """
        self.tasks = []
        self.owners = []
        if not os.path.exists(self.filename):
            self.owners = ["No Owner"]
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if lines and lines[0].startswith("OWNERS:"):
            self.owners = [o for o in lines[0].strip().replace("OWNERS:", "").split(",") if o]
            if not self.owners:
                self.owners = ["No Owner"]
            task_lines = lines[1:]
        else:
            self.owners = ["No Owner"]
            task_lines = lines
        for line in task_lines:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                task_text = parts[0]
                owner = parts[1]
                done = parts[2] in ("True", "1")
                date_done = parts[3] if len(parts) > 3 and parts[3] else None
                self.tasks.append((task_text, owner, done, date_done))

    def add_owner(self, owner):
        """
        Add a new owner to the list of owners.

        Args:
            owner (str): The owner to add.
        """
        if owner and owner not in self.owners:
            self.owners.append(owner)
            self.save_tasks()
