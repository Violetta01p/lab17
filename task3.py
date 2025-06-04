# Додати у метод load_notes класу Assistant з завдання 1:

def load_notes(self):
    if os.path.exists(self.filename):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.notes = json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Файл notes.json пошкоджено. Створюємо новий файл.")
            self.notes = []
            self.save_notes()
    else:
        self.notes = []
        self.save_notes()
