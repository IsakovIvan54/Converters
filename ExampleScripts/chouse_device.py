import tkinter as tk

def on_select():
    print("Selected option:", selected_option.get())

root = tk.Tk()
root.title("Radio Buttons Example")

# a = selected_option.get

# Create a variable to store the selected option
selected_option = tk.StringVar()

# Set the default value to "Source 150V"
selected_option.set("Source 150V")
a = selected_option.get()

# Create a radio button for "Source 150V"
option1 = tk.Radiobutton(root, text="Source 150V", variable=selected_option, value="Source 150V", command=on_select)
option1.pack()

# Create a radio button for "Source 600V"
option2 = tk.Radiobutton(root, text="Source 600V", variable=selected_option, value="Source 600V", command=on_select)
option2.pack()

root.mainloop()