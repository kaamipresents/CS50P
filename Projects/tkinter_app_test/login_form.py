import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Login")

tk.Label(window, text="Username").grid(row=0, column=0)
tk.Label(window, text="Password").grid(row=1, column=0)

username = tk.Entry(window)
password = tk.Entry(window, show="*")

username.grid(row=0, column=1)
password.grid(row=1, column=1)

def login():
    if not username.get() or not password.get():
        messagebox.showerror("Error", "Please enter both username and password")
        return
    else:
        user_value = username.get()
        password_value = password.get()
        messagebox.showinfo("Login", "Login successful!")
        messagebox.showinfo("Welcome",f"Welcome, {user_value}!")
        window.destroy()

button = tk.Button(window, text="Login", command=login)
button.grid(row=2, column=1)

window.mainloop()