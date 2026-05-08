#Author: Chanugi Weerakoon
#Date: 13th April 2025
#Task Manager

import json 
import tkinter as tk 
from tkinter import ttk 

#Task Class
class Task: 
    def __init__(self, task_name, task_description, priority, due_date): 
        self.task_name = task_name 
        self.task_description = task_description 
        self.priority = priority 
        self.due_date = due_date 

    def to_dict(self):
        return { 
            "name": self.task_name, 
            "description": self.task_description, 
            "priority": self.priority, 
            "due_date": self.due_date 
        }

# Task Manager Class
class TaskManager: 
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.task_list = [] 
        self.load_tasks() 

    def load_tasks(self): 
        try: 
            with open(self.filename, 'r') as f: 
                data = json.load(f) 
                self.task_list = [Task(item["name"], item["description"], item["priority"], item["due_date"]) for item in data]  
        except Exception as e:
            print(f"Error loading tasks: {e}") #debugging info
            self.task_list = [] 
            
    def filter_tasks(self, name=None, priority=None, date=None): 
        result = self.task_list 
        if name: 
            result = [t for t in result if name.lower() in t.task_name.lower()] 
        if priority: 
            result = [t for t in result if t.priority.lower() == priority.lower()] 
        if date: 
            result = [t for t in result if t.due_date == date] 
        return result 

    def sort_tasks(self, key='task_name'): 
        self.task_list.sort(key=lambda t: getattr(t, key).lower()) 

# Task Manager UI class
class TaskManagerUI:
    def __init__(self, window):
        self.window = window
        self.window.title("My Task Manager")
        self.controller = TaskManager()
        self.setup()
        self.show_tasks()

    def setup(self):
        # Filters
        tk.Label(self.window, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Priority Level").grid(row=0, column=2)
        self.priority_combo = ttk.Combobox(self.window, values=["", "High", "Medium", "Low"], width=10)
        self.priority_combo.grid(row=0, column=3)

        tk.Label(self.window, text="Due Date (YYYY-MM-DD)").grid(row=0, column=4)
        self.date_entry = tk.Entry(self.window)
        self.date_entry.grid(row=0, column=5)

        tk.Button(self.window, text="Filter", command=self.apply_filter).grid(row=0, column=6)

        # TreeView setup
        cols = ("task_name", "task_description", "priority", "due_date")
        self.tree = ttk.Treeview(self.window, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").capitalize(), command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=150)
        self.tree.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

    def show_tasks(self, tasks=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tasks = tasks if tasks else self.controller.task_list
        for t in tasks:
            self.tree.insert("", "end", values=(t.task_name, t.task_description, t.priority, t.due_date))

    def apply_filter(self):
        name = self.name_entry.get()
        priority = self.priority_combo.get()
        date = self.date_entry.get()
        filtered = self.controller.filter_tasks(name, priority, date)
        self.show_tasks(filtered)

    def sort_by(self, key):
        self.controller.sort_tasks(key)
        self.show_tasks()

# Run the app
if __name__ == "__main__":
    window = tk.Tk()
    app = TaskManagerUI(window)
    window.mainloop()

