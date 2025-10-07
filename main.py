import tkinter as tk
from tkinter import scrolledtext
import os
import socket
import argparse # Добавили для парсинга аргументов

class ShellEmulator(tk.Tk):
    def __init__(self, vfs_path=None, custom_prompt=None, script_path=None):
        super().__init__()
        # --- Параметры конфигурации ---
        self.vfs_path = vfs_path
        self.custom_prompt = custom_prompt
        self.script_path = script_path

        # --- Настройка окна ---
        self.title(self.get_window_title())
        self.geometry("800x600")

        # --- Виджеты ---
        self.output_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
        self.output_area.pack(expand=True, fill='both')
        self.output_area.configure(state='disabled')

        input_frame = tk.Frame(self, bg="black")
        input_frame.pack(fill='x')

        self.prompt_label = tk.Label(input_frame, text=self.get_prompt(), bg="black", fg="lightgreen")
        self.prompt_label.pack(side='left', padx=(5, 0))

        self.entry = tk.Entry(input_frame, bg="black", fg="white", insertbackground="white", borderwidth=0)
        self.entry.pack(expand=True, fill='x')
        self.entry.focus()

        # --- Привязка событий ---
        self.entry.bind("<Return>", self.handle_user_input)

        self.display_message("Shell Emulator started. Type 'exit' to close.")
        
        # Вывод отладочной информации о конфигурации
        self.display_config()

        # Если указан скрипт, выполняем его
        if self.script_path:
            self.run_startup_script()

    def get_window_title(self):
        try:
            username = os.getlogin()
        except OSError:
            username = "user"
        hostname = socket.gethostname()
        return f"Эмулятор - [{username}@{hostname}]"

    def get_prompt(self):
        # Используем пользовательское приглашение, если оно есть
        return self.custom_prompt if self.custom_prompt is not None else "$ "

    def display_config(self):
        """Выводит заданные параметры при запуске."""
        self.display_message("--- Configuration ---")
        self.display_message(f"VFS Path: {self.vfs_path or 'Not set'}")
        self.display_message(f"Custom Prompt: {self.custom_prompt or 'Default'}")
        self.display_message(f"Startup Script: {self.script_path or 'Not set'}")
        self.display_message("---------------------")

    def display_message(self, message, is_input=False):
        self.output_area.configure(state='normal')
        if is_input:
            # Отображаем ввод с текущим промптом
            prompt = self.prompt_label.cget("text")
            self.output_area.insert(tk.END, prompt + message + "\n")
        else:
            self.output_area.insert(tk.END, message + "\n")
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)

    def run_startup_script(self):
        """Читает и выполняет команды из стартового скрипта."""
        self.display_message(f"Executing script: {self.script_path}")
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # В Python комментарии - это '#'
                    command_line = line.strip()
                    if command_line and not command_line.startswith("#"):
                        # Имитируем диалог: показываем ввод, затем выполняем
                        self.display_message(command_line, is_input=True)
                        self.process_command(command_line)
        except FileNotFoundError:
            self.display_message(f"Error: Script file not found at '{self.script_path}'")
        except Exception as e:
            self.display_message(f"Error executing script: {e}")
        self.display_message("Script execution finished.")


    def handle_user_input(self, event=None):
        """Обрабатывает ввод пользователя из GUI."""
        command_line = self.entry.get()
        if not command_line:
            return
        
        self.display_message(command_line, is_input=True)
        self.entry.delete(0, tk.END)
        self.process_command(command_line)

    def process_command(self, command_line):
        """Обрабатывает одну строку с командой."""
        parts = command_line.strip().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]

        if command == "exit":
            self.quit()
        elif command == "ls":
            self.display_message(f"Command: {command}, Args: {args}")
        elif command == "cd":
            self.display_message(f"Command: {command}, Args: {args}")
        else:
            self.display_message(f"Error: Unknown command '{command}'")

def main():
    """Главная функция для парсинга аргументов и запуска приложения."""
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument(
        '--vfs',
        type=str,
        help="Path to the Virtual File System (VFS) source file."
    )
    parser.add_argument(
        '--prompt',
        type=str,
        help="Custom prompt to be displayed in the REPL."
    )
    parser.add_argument(
        '--script',
        type=str,
        help="Path to the startup script to execute."
    )
    args = parser.parse_args()

    app = ShellEmulator(
        vfs_path=args.vfs,
        custom_prompt=args.prompt,
        script_path=args.script
    )
    app.mainloop()

if __name__ == "__main__":
    main()