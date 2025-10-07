import csv
import os

class VFS:
    def __init__(self):
        self.fs = {} # Файловая система: {'/path/to/file': {'type': 'file', 'content': '...'} }
        self.cwd = "/" # Текущая рабочая директория

    def load_from_csv(self, csv_path):
        """Загружает структуру VFS из CSV файла."""
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Сбрасываем текущую ФС и ставим корень
                self.fs = {"/": {"type": "dir", "content": None}}
                for row in reader:
                    path, type, content = row
                    if path != "/": # Корень уже есть
                        self.fs[path] = {"type": type, "content": content if type == 'file' else None}
            return True, f"VFS loaded from {csv_path}"
        except FileNotFoundError:
            return False, f"Error: VFS file not found at '{csv_path}'"
        except Exception as e:
            return False, f"Error parsing VFS file: {e}"

    def create_default(self):
        """Создает VFS по умолчанию в памяти."""
        self.fs = {
            "/": {"type": "dir", "content": None},
            "/default_dir": {"type": "dir", "content": None},
            "/default_file.txt": {"type": "file", "content": "This is a default file."},
        }
        return "Default VFS created in memory."

    def get_full_path(self, path):
        """Преобразует относительный путь в абсолютный."""
        if os.path.isabs(path):
            return os.path.normpath(path).replace('\\', '/')
        # os.path.join ведет себя не совсем так, как нужно для VFS, поэтому делаем вручную
        combined = os.path.normpath(os.path.join(self.cwd, path)).replace('\\', '/')
        return combined