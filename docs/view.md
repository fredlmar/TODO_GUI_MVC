# View

Das View-Modul (`view.py`) stellt die grafische Oberfläche bereit und nimmt Benutzereingaben entgegen.

## Hauptkomponenten

- Eingabefeld für Aufgaben
- Buttons zum Hinzufügen, Löschen und Speichern
- Listbox zur Anzeige der Aufgaben

## API-Dokumentation

::: view.TaskView
    handler: python
    selection:
      members:
        - get_input
        - clear_input
        - update_tasks
        - get_selected_index
