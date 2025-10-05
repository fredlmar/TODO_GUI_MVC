# view.py

import tkinter as tk

class TaskView(tk.Frame):
    def update_owner_dropdown(self, selected_owner=None):
        """
        Refresh the owner OptionMenu with the current owner_options list.
        Optionally set the selected owner.
        """
        menu = self.owner_menu['menu']
        menu.delete(0, 'end')
        for owner in self.owner_options:
            menu.add_command(label=owner, command=tk._setit(self.owner_var, owner))
        if selected_owner and selected_owner in self.owner_options:
            self.owner_var.set(selected_owner)
        elif self.owner_options:
            self.owner_var.set(self.owner_options[0])
    """
    View for the TO-DO List GUI application.
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
        # Set window width based on the task listbox width (50 chars) and font size
        listbox_width_chars = 50
        # Estimate: 1 char ~6 px, plus border and scrollbar (right-aligned)
        window_width = int(listbox_width_chars * 6 + 20)  # 6px per char, 20px border
        window_height = 400
        self.master.geometry(f"{window_width}x{window_height}")
        # Add minimal left/right border, anchor all to west (left)
        self.pack(padx=(8,8), pady=20, anchor="w")

        # Add menu bar
        self._create_menu_bar()
    def _create_menu_bar(self):
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        # Info menu
        info_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Info", menu=info_menu)
        info_menu.add_command(label="About", command=self.controller.show_info)

        # Task entry row
        entry_row = tk.Frame(self)
        entry_row.pack(pady=2, fill="x")
        tk.Label(entry_row, text="Task:").pack(side=tk.LEFT)
        self.task_entry = tk.Entry(entry_row, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=2)
        # Move Add Task button to the left of the task input field
        self.add_task_button = tk.Button(entry_row, text="Add Task", command=self.controller.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=2)

        # Owner row
        owner_row = tk.Frame(self)
        owner_row.pack(pady=2, fill="x")
        tk.Label(owner_row, text="Owner:").pack(side=tk.LEFT)

        # Initialize owner options from file/model
        self.owner_options = self.controller.model.owners.copy()
        owner_menu_values = self.owner_options if self.owner_options else ["No Owner"]

        self.owner_var = tk.StringVar()
        self.owner_menu = tk.OptionMenu(owner_row, self.owner_var, *owner_menu_values)
        self.owner_menu.pack(side=tk.LEFT, padx=2)

        # Set default owner selection
        if self.owner_options:
            self.owner_var.set(self.owner_options[0])
        else:
            self.owner_var.set("No Owner")

        self.new_owner_entry = tk.Entry(owner_row, width=15)
        self.new_owner_entry.pack(side=tk.LEFT, padx=2)
        self.add_owner_button = tk.Button(owner_row, text="Add Owner", command=self.controller.add_owner)
        self.add_owner_button.pack(side=tk.LEFT, padx=2)

        # Change owner button on a new row
        change_owner_row = tk.Frame(self)
        change_owner_row.pack(pady=2, anchor="w")
        self.modify_owner_button = tk.Button(change_owner_row, text="Change Task Owner", command=self.controller.modify_owner)
        self.modify_owner_button.pack(side=tk.LEFT, padx=2)

        self.filter_var = tk.BooleanVar(value=False)
        self.filter_checkbox = tk.Checkbutton(self, text="Filter by Selected Owner", variable=self.filter_var, command=self.controller.toggle_owner_filter)
        self.filter_checkbox.pack(pady=2, anchor="w")

        # Tasks listbox
        self.tasks_listbox = tk.Listbox(self, width=50)
        self.tasks_listbox.pack(pady=5, anchor="w")

        # Row for done and delete buttons
        action_row = tk.Frame(self)
        action_row.pack(pady=2, fill="x")
        self.done_button = tk.Button(action_row, text="Set Task to Done", command=self.controller.set_task_done)
        self.done_button.pack(side=tk.LEFT, padx=2)
        self.delete_button = tk.Button(action_row, text="Delete Task", command=self.controller.delete_task)
        self.delete_button.pack(side=tk.RIGHT, padx=2, anchor="e")

        self.save_button = tk.Button(self, text="Save", command=self.controller.save_tasks)
        self.save_button.pack(anchor="e", pady=5, fill="x")

        # Trace owner_var to update list if filtering is enabled (after all widgets are created)
        self.owner_var.trace_add('write', lambda *args: self._on_owner_change())

    def add_owner(self):
        """
        Add a new owner to the dropdown and refresh the OptionMenu.
        """
        new_owner = self.new_owner_entry.get().strip()
        if new_owner and new_owner not in self.owner_options:
            self.owner_options.append(new_owner)
            self.update_owner_dropdown(selected_owner=new_owner)


    def _on_owner_change(self):
        if hasattr(self, 'filter_var') and self.filter_var.get():
            self.controller.toggle_owner_filter()

    def set_owner_dropdown(self, owner):
        """
        Set the owner dropdown to the given owner.
        """
        self.update_owner_dropdown(selected_owner=owner)

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
            # Support (task_text, owner, done, date_done), (task_text, owner, done), or (task_text, owner)
            if isinstance(task, tuple):
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
                    continue
                if filter_owner is None or owner == filter_owner:
                    status = "[DONE] " if done else ""
                    date_str = f" (Done: {date_done})" if done and date_done else ""
                    display = f"{status}{task_text} (Owner: {owner}){date_str}"
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
