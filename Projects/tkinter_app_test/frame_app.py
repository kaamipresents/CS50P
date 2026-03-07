import tkinter as tk

window = tk.Tk()
window.geometry("500x400")

header = tk.Frame(window, bg="lightblue", height=50)
header.pack(fill="x")

content = tk.Frame(window, bg="white")
content.pack(fill="both", expand=True)

footer = tk.Frame(window, bg="lightgray", height=40)
footer.pack(fill="x")

tk.Label(header, text="Header").pack()
tk.Label(content, text="Content Area").pack()
tk.Label(footer, text="Footer").pack()

window.mainloop()