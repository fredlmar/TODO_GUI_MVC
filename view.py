# view.py

import tkinter as tk

class TaskView(tk.Frame):
    """
    View for the To-Do List GUI application.

    Provides the graphical interface and user input elements.
    """
    # Duplicate __init__ removed. Only one __init__ method should exist, and it should include all widgets, including the filter button.
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
        # Set window width based on the task listbox width (50 chars) and font size
        listbox_width_chars = 50
        # Estimate: 1 char ~6 px, plus border and scrollbar (right-aligned)
        window_width = int(listbox_width_chars * 6 + 20)  # 8px per char, 28px border
        window_height = 400
        self.master.geometry(f"{window_width}x{window_height}")
        # Add minimal left/right border, anchor all to west (left)
        self.pack(padx=(8,8), pady=20, anchor="w")

        # Task input row (entry and add button in one line), aligned with task listbox
        task_row = tk.Frame(self)
        task_row.pack(pady=5, anchor="w")
        self.task_entry = tk.Entry(task_row, width=40)
        self.task_entry.pack(side=tk.LEFT, anchor="w")
        self.add_button = tk.Button(task_row, text="Add Task", command=self.controller.add_task)
        self.add_button.pack(side=tk.LEFT, padx=2, anchor="w")


        # Owner selection row (label, dropdown, and change button in one line)
        owner_row = tk.Frame(self)
        owner_row.pack(pady=2, anchor="w")
        self.owner_label = tk.Label(owner_row, text="Owner:")
        self.owner_label.pack(side=tk.LEFT)
        self.owner_var = tk.StringVar()
        self.owner_var.set("Alice")  # Default owner
        self.owner_options = ["Alice", "Bob", "Charlie", "Manfredo", "David", "Eve"]
        self.owner_menu = tk.OptionMenu(owner_row, self.owner_var, *self.owner_options)
        self.owner_menu.pack(side=tk.LEFT, padx=2)
        self.modify_owner_button = tk.Button(owner_row, text="Change Owner of Selected Task", command=self.controller.modify_owner)
        self.modify_owner_button.pack(side=tk.LEFT, padx=2)





        self.filter_var = tk.BooleanVar(value=False)
        self.filter_checkbox = tk.Checkbutton(self, text="Show Only Selected Owner's Tasks", variable=self.filter_var, command=self.controller.toggle_owner_filter)
        self.filter_checkbox.pack(pady=2, anchor="w")


        self.tasks_listbox = tk.Listbox(self, width=50)
        self.tasks_listbox.pack(pady=5, anchor="w")

        # Row for done and delete buttons
        action_row = tk.Frame(self)
        action_row.pack(pady=2, fill="x")
        self.done_button = tk.Button(action_row, text="Set Selected Task to Done", command=self.controller.set_task_done)
        self.done_button.pack(side=tk.LEFT, padx=2)
        self.delete_button = tk.Button(action_row, text="Delete Selected Task", command=self.controller.delete_task)
        self.delete_button.pack(side=tk.RIGHT, padx=2, anchor="e")


        self.save_button = tk.Button(self, text="Save Tasks", command=self.controller.save_tasks)
        self.save_button.pack(anchor="e", pady=5, fill="x")


        # Trace owner_var to update list if filtering is enabled (after all widgets are created)
        self.owner_var.trace_add('write', lambda *args: self._on_owner_change())

    def _on_owner_change(self):
        if hasattr(self, 'filter_var') and self.filter_var.get():
            self.controller.toggle_owner_filter()


    def set_owner_dropdown(self, owner):
        """
        Set the owner dropdown to the given owner.
        """
        if owner in self.owner_options:
            self.owner_var.set(owner)
        else:
            self.owner_var.set(self.owner_options[0])

    def get_input(self):
        """
        Get the current text from the input field.

        Returns:
            tuple: (task text, owner)
        """
        return (self.task_entry.get(), self.owner_var.get())

    def clear_input(self):
        """
        Clear the input field.
        """
        self.task_entry.delete(0, tk.END)

    def update_tasks(self, tasks, filter_owner=None, selected_index=None):
        """
        Update the listbox to show all current tasks, optionally filtering by owner.

        Args:
            tasks (list): The list of tasks to display.
            filter_owner (str, optional): If set, only show tasks for this owner.
            selected_index (int, optional): Index to re-select after update.
        """
        self.tasks_listbox.delete(0, tk.END)
        for task in tasks:
            # Support (task_text, owner, done) or (task_text, owner)
            if isinstance(task, tuple):
                if len(task) == 3:
                    task_text, owner, done = task
                elif len(task) == 2:
                    task_text, owner = task
                    done = False
                else:
                    continue
                if filter_owner is None or owner == filter_owner:
                    status = "[DONE] " if done else ""
                    display = f"{status}{task_text} (Owner: {owner})"
                    self.tasks_listbox.insert(tk.END, display)
            else:
                if filter_owner is None:
                    self.tasks_listbox.insert(tk.END, str(task))

        # Restore selection if possible
        if selected_index is not None and self.tasks_listbox.size() > 0:
            if 0 <= selected_index < self.tasks_listbox.size():
                self.tasks_listbox.selection_set(selected_index)
                self.tasks_listbox.activate(selected_index)
                self.tasks_listbox.see(selected_index)


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
