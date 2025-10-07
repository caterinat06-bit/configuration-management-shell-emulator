import tkinter as tk
from tkinter import scrolledtext
import os
import socket

class ShellEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        # --- Настройка окна ---
        self.title(self.get_window_title())
        self.geometry("800x600")

        # --- Виджеты ---
        # Поле для вывода текста (лог команд)
        self.output_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
        self.output_area.pack(expand=True, fill='both')
        self.output_area.configure(state='disabled') # Запрещаем прямой ввод

        # Фрейм для строки ввода и метки
        input_frame = tk.Frame(self, bg="black")
        input_frame.pack(fill='x')

        # Метка приглашения
        self.prompt_label = tk.Label(input_frame, text=self.get_prompt(), bg="black", fg="lightgreen")
        self.prompt_label.pack(side='left', padx=(5, 0))

        # Строка для ввода команд
        self.entry = tk.Entry(input_frame, bg="black", fg="white", insertbackground="white", borderwidth=0)
        self.entry.pack(expand=True, fill='x')
        self.entry.focus()

        # --- Привязка событий ---
        self.entry.bind("<Return>", self.execute_command)

        self.display_message("Shell Emulator started. Type 'exit' to close.")

    def get_window_title(self):
        """Формирует заголовок окна на основе данных ОС."""
        try:
            username = os.getlogin()
        except OSError:
            username = "user"
        hostname = socket.gethostname()
        return f"Эмулятор - [{username}@{hostname}]"

    def get_prompt(self):
        """Возвращает стандартное приглашение к вводу."""
        return "$ "

    def display_message(self, message, is_input=False):
        """Отображает сообщение в поле вывода."""
        self.output_area.configure(state='normal')
        if is_input:
            self.output_area.insert(tk.END, self.get_prompt() + message + "\n")
        else:
            self.output_area.insert(tk.END, message + "\n")
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END) # Автопрокрутка вниз

    def execute_command(self, event=None):
        """Выполняет введенную команду."""
        command_line = self.entry.get()
        if not command_line:
            return

        self.display_message(command_line, is_input=True)
        self.entry.delete(0, tk.END)

        # Простой парсер: команда и аргументы
        parts = command_line.strip().split()
        command = parts[0]
        args = parts[1:]

        # --- Обработка команд ---
        if command == "exit":
            self.quit()
        elif command == "ls":
            # Заглушка для ls
            self.display_message(f"Command: {command}, Args: {args}")
        elif command == "cd":
            # Заглушка для cd
            self.display_message(f"Command: {command}, Args: {args}")
        else:
            self.display_message(f"Error: Unknown command '{command}'")

if __name__ == "__main__":
    app = ShellEmulator()
    app.mainloop()