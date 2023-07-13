import tkinter as tk

def toggle_flag():
    if flag_var.get() == 1:
        print("Flag is ON")
    else:
        print("Flag is OFF")

root = tk.Tk()

flag_var = tk.IntVar()

checkbox = tk.Checkbutton(root, text="Flag", variable=flag_var, command=toggle_flag)
checkbox.pack()

root.mainloop()