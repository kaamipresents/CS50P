import tkinter as tk

window = tk.Tk()
window.geometry("600x400")

sidebar = tk.Frame(window, bg="lightgray", width=150)
sidebar.pack(side="left", fill="y")

content = tk.Frame(window, bg="white")
content.pack(side="right", fill="both", expand=True)

tk.Label(sidebar, text="Menu").pack(pady=10)
tk.Label(content, text="Main Content").pack()

window.mainloop()