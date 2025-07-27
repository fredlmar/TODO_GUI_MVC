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
            task (str): The task to add.
        """
        if task:
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
                    f.write(task + "\n")
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
                self.tasks = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.tasks = []
        except Exception:
            self.tasks = []
