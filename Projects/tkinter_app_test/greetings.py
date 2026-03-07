import tkinter as tk

# window create
window = tk.Tk()
window.title("Greeting App")
window.geometry("300x200")

# label
label = tk.Label(window, text="Enter your name:")
label.pack()

# entry input
entry = tk.Entry(window)
entry.pack()

# button event
def greet():
    name = entry.get()
    result_label.config(text=f"Hello {name}")

button = tk.Button(window, text="Greet", command=greet)
button.pack()

# result label
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()