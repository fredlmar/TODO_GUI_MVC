# Model

Das Model (`model.py`) verwaltet die Aufgabenliste und die Speicherung/Ladung aus einer Datei.

## Hauptmethoden

- `add_task(task)`: Fügt eine Aufgabe hinzu.
- `get_tasks()`: Gibt alle Aufgaben zurück.
- `delete_task(index)`: Löscht eine Aufgabe.
- `save_tasks(filename)`: Speichert Aufgaben in einer Datei.
- `load_tasks(filename)`: Lädt Aufgaben aus einer Datei.

## API-Dokumentation

::: model.TaskModel
    handler: python
    selection:
      members:
        - add_task
        - get_tasks
        - delete_task
        - save_tasks
        - load_tasks
