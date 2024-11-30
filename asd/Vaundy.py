import tkinter as tk
from tkinter import messagebox, ttk
import json

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Todo List App")
        self.master.geometry("400x500")

        self.tasks = {}  # Change this to: self.tasks = {}
        self.private_tasks = []

        self.load_tasks()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Normal Tasks Tab
        self.normal_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.normal_frame, text="Normal Tasks")

        self.task_entry = tk.Entry(self.normal_frame, width=40)
        self.task_entry.pack(pady=10)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(self.normal_frame, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.pack()

        self.add_button = tk.Button(self.normal_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(self.normal_frame, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.remove_button = tk.Button(self.normal_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

        # Private Tasks Tab
        self.private_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.private_frame, text="Private Notes")

        self.private_entry = tk.Entry(self.private_frame, width=40, show="*")
        self.private_entry.pack(pady=10)

        self.add_private_button = tk.Button(self.private_frame, text="Add Private Note", command=self.add_private_task)
        self.add_private_button.pack()

        self.private_listbox = tk.Listbox(self.private_frame, width=50, height=10)
        self.private_listbox.pack(pady=10)

        self.remove_private_button = tk.Button(self.private_frame, text="Remove Private Note", command=self.remove_private_task)
        self.remove_private_button.pack()

        self.update_listboxes()

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task:
            self.tasks[task] = priority  # Store task with priority
            self.task_entry.delete(0, tk.END)
            self.update_listboxes()
            self.save_tasks()

    def remove_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = list(self.tasks.keys())[index]
            del self.tasks[task]
            self.update_listboxes()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def add_private_task(self):
        task = self.private_entry.get()
        if task:
            self.private_tasks.append(task)
            self.private_entry.delete(0, tk.END)
            self.update_listboxes()
            self.save_tasks()

    def remove_private_task(self):
        try:
            index = self.private_listbox.curselection()[0]
            del self.private_tasks[index]
            self.update_listboxes()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a private note to remove.")

    def update_listboxes(self):
        self.task_listbox.delete(0, tk.END)
        sorted_tasks = sorted(self.tasks.items(), key=lambda x: self.priority_order(x[1]), reverse=True)
        for task, priority in sorted_tasks:
            self.task_listbox.insert(tk.END, f"[{priority}] {task}")

        self.private_listbox.delete(0, tk.END)
        for task in self.private_tasks:
            self.private_listbox.insert(tk.END, "*" * len(task))

    def priority_order(self, priority):
        order = {"High": 3, "Medium": 2, "Low": 1}
        return order.get(priority, 0)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump({"tasks": self.tasks, "private_tasks": self.private_tasks}, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", {})
                self.private_tasks = data.get("private_tasks", [])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
