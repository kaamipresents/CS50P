import tkinter as tk
from tkinter import messagebox

def say_hello():
    entry_value = entry.get() # get the value from the entry widget
    if entry_value: # check if the entry value is not empty
        messagebox.showinfo("Greeting", f"Hello {entry_value}") # show a message box with the greeting message

root = tk.Tk() # creating a window
root.title("Testing App") # setting the title of the window
root.geometry("400x300") # setting the size of the window (width x height)

# widget creation
label = tk.Label(root, text="User Email")
label.grid(row=0, column=0) # adding the label to the window

# entry creation
entry = tk.Entry(root)
entry.grid(row=0, column=1) # adding the entry to the window

# button creation
button = tk.Button(root, text="Click Me", command=say_hello)
button.grid(row=1, column=0, columnspan=1) # adding the button to the window and spanning it across two columns 

root.mainloop() # this line starts the event loop, which keeps the window open and responsive to user interactions.