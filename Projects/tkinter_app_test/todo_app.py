import tkinter as tk

window = tk.Tk()
window.title("Todo App")
window.geometry("300x400")

entry = tk.Entry(window)
entry.pack()

listbox = tk.Listbox(window)
listbox.pack()

def add_task():
    if entry.get():
        task = entry.get()
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)

button = tk.Button(window, text="Add Task", command=add_task)
button.pack()

window.mainloop()