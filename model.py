# model.py

class TaskModel:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if task:
            self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False

    def save_tasks(self, filename="tasks.txt"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for task in self.tasks:
                    f.write(task + "\n")
            return True
        except Exception:
            return False

    def load_tasks(self, filename="tasks.txt"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.tasks = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.tasks = []
        except Exception:
            self.tasks = []
