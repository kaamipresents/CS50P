import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.title("Simple Notepad")
window.geometry("700x500")

# Text Area
text_area = tk.Text(window, wrap="word")
text_area.pack(fill="both", expand=True, side="left")

# Scrollbar
scrollbar = tk.Scrollbar(window, command=text_area.yview)
scrollbar.pack(side="right", fill="y")

text_area.config(yscrollcommand=scrollbar.set)


# ---------- File Functions ----------

def new_file():
    text_area.delete(1.0, tk.END)


def open_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        with open(file_path, "r") as file:
            content = file.read()

        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")

    if file_path:
        content = text_area.get(1.0, tk.END)

        with open(file_path, "w") as file:
            file.write(content)


# ---------- Edit Functions ----------

def cut_text():
    text_area.event_generate("<<Cut>>")


def copy_text():
    text_area.event_generate("<<Copy>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


# ---------- Word Wrap ----------

wrap_on = True

def toggle_wrap():
    global wrap_on

    if wrap_on:
        text_area.config(wrap="none")
        wrap_on = False
    else:
        text_area.config(wrap="word")
        wrap_on = True


# ---------- Status Bar ----------

status_bar = tk.Label(window, text="Line: 1 | Column: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")


def update_status(event=None):
    cursor_position = text_area.index(tk.INSERT)

    line, column = cursor_position.split(".")

    status_bar.config(text=f"Line: {line} | Column: {column}")


text_area.bind("<KeyRelease>", update_status)
text_area.bind("<ButtonRelease>", update_status)


# ---------- Menu Bar ----------

menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)

view_menu.add_command(label="Toggle Word Wrap", command=toggle_wrap)


# ---------- Keyboard Shortcuts ----------

window.bind("<Control-n>", lambda event: new_file())
window.bind("<Control-o>", lambda event: open_file())
window.bind("<Control-s>", lambda event: save_file())
window.bind("<Control-c>", lambda event: copy_text())
window.bind("<Control-v>", lambda event: paste_text())
window.bind("<Control-x>", lambda event: cut_text())


window.mainloop()