import tkinter as tk
from tkinter import scrolledtext
import os
import socket
import argparse
from vfs import VFS 

class ShellEmulator(tk.Tk):
    def __init__(self, vfs_path=None, custom_prompt=None, script_path=None):
        super().__init__()
        # --- VFS ---
        self.vfs = VFS()
        if vfs_path:
            is_loaded, message = self.vfs.load_from_csv(vfs_path)
            self.initial_message = message
        else:
            # Если путь не указан, создаем VFS по умолчанию
            self.initial_message = self.vfs.create_default()

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
        self.display_message(self.initial_message)
        self.display_config()

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
        # Обновляем промпт, чтобы включить текущую директорию
        base_prompt = self.custom_prompt if self.custom_prompt is not None else "$"
        return f"{self.vfs.cwd} {base_prompt} "

    def update_prompt(self):
        """Обновляет текст метки приглашения."""
        self.prompt_label.config(text=self.get_prompt())

    def display_config(self):
        self.display_message("--- Configuration ---")
        self.display_message(f"VFS Path: {self.vfs_path or 'Default in-memory'}")
        self.display_message(f"Custom Prompt: {self.custom_prompt or 'Default'}")
        self.display_message(f"Startup Script: {self.script_path or 'Not set'}")
        self.display_message("---------------------")

    def display_message(self, message, is_input=False):
        self.output_area.configure(state='normal')
        if is_input:
            prompt = self.prompt_label.cget("text")
            self.output_area.insert(tk.END, prompt + message + "\n")
        else:
            self.output_area.insert(tk.END, message + "\n")
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)
    
    def run_startup_script(self):
        self.display_message(f"Executing script: {self.script_path}")
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    command_line = line.strip()
                    if command_line and not command_line.startswith("#"):
                        self.display_message(command_line, is_input=True)
                        self.process_command(command_line)
                        self.update() # Обновляем GUI, чтобы видеть вывод
        except FileNotFoundError:
            self.display_message(f"Error: Script file not found at '{self.script_path}'")
        except Exception as e:
            self.display_message(f"Error executing script: {e}")
        self.display_message("Script execution finished.")
        self.update_prompt()

    def handle_user_input(self, event=None):
        command_line = self.entry.get()
        if not command_line:
            return
        
        self.display_message(command_line, is_input=True)
        self.entry.delete(0, tk.END)
        self.process_command(command_line)
        self.update_prompt()

    def process_command(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]

        # --- Словарь команд ---
        commands = {
            "exit": self.cmd_exit,
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
        }

        if command in commands:
            commands[command](args)
        else:
            self.display_message(f"Error: Unknown command '{command}'")

    # --- Реализации команд ---
    def cmd_exit(self, args):
        self.quit()

    def cmd_ls(self, args):
        # Заглушка, реальная логика будет в следующем этапе
        self.display_message(f"Command: ls, Args: {args} (logic not implemented yet)")

    def cmd_cd(self, args):
        # Заглушка, реальная логика будет в следующем этапе
        self.display_message(f"Command: cd, Args: {args} (logic not implemented yet)")

def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument('--vfs', type=str, help="Path to the VFS source file.")
    parser.add_argument('--prompt', type=str, help="Custom prompt.")
    parser.add_argument('--script', type=str, help="Path to the startup script.")
    args = parser.parse_args()

    app = ShellEmulator(vfs_path=args.vfs, custom_prompt=args.prompt, script_path=args.script)
    app.mainloop()

if __name__ == "__main__":
    main()