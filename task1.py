import json
import os

class Assistant:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.notes = []
                self.save_notes()
        else:
            self.notes = []
            self.save_notes()

    def save_notes(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()

    def list_notes(self):
        return self.notes

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.lower()]

def main():
    assistant = Assistant()
    print("Консольний асистент. Команди: /add, /list, /search, /exit")

    while True:
        command = input("Введіть команду: ").strip()
        if command == "/add":
            note = input("Введіть текст нотатки: ").strip()
            assistant.add_note(note)
            print("Нотатку додано.")
        elif command == "/list":
            notes = assistant.list_notes()
            if notes:
                print("Ваші нотатки:")
                for i, note in enumerate(notes, 1):
                    print(f"{i}. {note}")
            else:
                print("Нотаток немає.")
        elif command == "/search":
            keyword = input("Введіть ключове слово для пошуку: ").strip()
            results = assistant.search_notes(keyword)
            if results:
                print("Знайдені нотатки:")
                for i, note in enumerate(results, 1):
                    print(f"{i}. {note}")
            else:
                print("Нотатки не знайдено.")
        elif command == "/exit":
            print("Вихід з програми.")
            break
        else:
            print("Невідома команда.")

if __name__ == "__main__":
    main()
