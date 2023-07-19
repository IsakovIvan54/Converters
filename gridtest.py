import tkinter as tk

root = tk.Tk()

# create a grid layout
root.grid()

# create an Entry widget
entry = tk.Entry(root, font=("Arial", 12))
entry.grid(row=0, column=0)

root.mainloop()