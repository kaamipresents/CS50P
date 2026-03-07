import tkinter as tk

window = tk.Tk()
window.title("Calculator")

entry1 = tk.Entry(window)
entry1.grid(row=0, column=0)

entry2 = tk.Entry(window)
entry2.grid(row=0, column=1)

def add():
    try:
        num1 = int(entry1.get())
        num2 = int(entry2.get())
    except ValueError:
        result.config(text="Invalid input")
        return
    result.config(text=f"Result: {num1 + num2}")

button = tk.Button(window, text="Add", command=add)
button.grid(row=1, column=0, columnspan=2)

result = tk.Label(window, text="")
result.grid(row=2, column=0, columnspan=2)

window.mainloop()