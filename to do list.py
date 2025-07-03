import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import threading
import time
import json

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except:
        return []

# Save tasks to file
def save_tasks():
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file)

# Check for reminders
def check_reminders():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for task in tasks:
            if task["reminder"] == now and not task["notified"]:
                messagebox.showinfo("Reminder", f"Reminder: {task['task']}")
                task["notified"] = True
                save_tasks()
        time.sleep(30)

def add_task():
    task_text = task_entry.get()
    if task_text:
        tasks.append({"task": task_text, "done": False, "reminder": "", "notified": False})
        update_listbox()
        task_entry.delete(0, tk.END)
        save_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        update_listbox()
        save_tasks()

def mark_complete():
    selected = listbox.curselection()
    if selected:
        tasks[selected[0]]["done"] = not tasks[selected[0]]["done"]
        update_listbox()
        save_tasks()

def update_task():
    selected = listbox.curselection()
    if selected:
        new_task = simpledialog.askstring("Update Task", "Enter new task text:")
        if new_task:
            tasks[selected[0]]["task"] = new_task
            update_listbox()
            save_tasks()

def set_reminder():
    selected = listbox.curselection()
    if selected:
        time_input = simpledialog.askstring("Set Reminder", "Enter reminder time (YYYY-MM-DD HH:MM):")
        try:
            datetime.datetime.strptime(time_input, "%Y-%m-%d %H:%M")
            tasks[selected[0]]["reminder"] = time_input
            tasks[selected[0]]["notified"] = False
            update_listbox()
            save_tasks()
        except ValueError:
            messagebox.showerror("Invalid Format", "Please use YYYY-MM-DD HH:MM format.")

def update_listbox():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        status = "✓" if task["done"] else "✗"
        reminder_info = f" [⏰ {task['reminder']}]" if task["reminder"] else ""
        listbox.insert(tk.END, f"{status} {task['task']}{reminder_info}")

# GUI setup
root = tk.Tk()
root.title("To-Do List with Reminder")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Mark Done", command=mark_complete).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Update", command=update_task).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Set Reminder", command=set_reminder).grid(row=0, column=4, padx=5)

listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

# Load tasks
tasks = load_tasks()
update_listbox()

# Start reminder thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

root.mainloop()
