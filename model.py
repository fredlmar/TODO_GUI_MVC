# model.py

class TaskModel:
    """
    Model for managing the list of tasks and file operations.

    Stores tasks in memory and provides methods to add, delete, save, and load tasks.
    """
    def __init__(self):
        """
        Initialize the TaskModel with an empty task list.
        """
        self.tasks = []

    def add_task(self, task):
        """
        Add a new task to the list.

        Args:
            task (tuple): The task to add, as (task_text, owner) or (task_text, owner, done).
        """
        if task and isinstance(task, tuple):
            if len(task) == 2:
                self.tasks.append((task[0], task[1], False))
            elif len(task) == 3:
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

    def save_tasks(self, filename="tasks.txt"):
        """
        Save all tasks to a text file.

        Args:
            filename (str): The file to save tasks to.

        Returns:
            bool: True if saving was successful, False otherwise.
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for task in self.tasks:
                    if isinstance(task, tuple):
                        if len(task) == 3:
                            f.write(f"{task[0]}|{task[1]}|{int(task[2])}\n")
                        elif len(task) == 2:
                            f.write(f"{task[0]}|{task[1]}|0\n")
                        else:
                            f.write(str(task) + "\n")
                    else:
                        f.write(str(task) + "\n")
            return True
        except Exception:
            return False

    def load_tasks(self, filename="tasks.txt"):
        """
        Load tasks from a text file.

        Args:
            filename (str): The file to load tasks from.
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.tasks = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) == 3:
                            text, owner, done = parts
                            self.tasks.append((text, owner, bool(int(done))))
                        elif len(parts) == 2:
                            self.tasks.append((parts[0], parts[1], False))
                        else:
                            self.tasks.append(line)
        except FileNotFoundError:
            self.tasks = []
        except Exception:
            self.tasks = []
