import tkinter as tk
from tkinter import messagebox

# Function to handle button click event
def save_settings():
    selected_option1 = dropdown1.get()
    selected_option2 = dropdown2.get()
    selected_option3 = dropdown3.get()

    # Save the selected options as defaults (you can modify this part as per your needs)
    with open("default_settings.txt", "w") as f:
        f.write(f"Option 1: {selected_option1}\n")
        f.write(f"Option 2: {selected_option2}\n")
        f.write(f"Option 3: {selected_option3}\n")

    messagebox.showinfo("Settings Saved", "Default settings have been saved successfully.")

# Create the main window
window = tk.Tk()
window.title("Settings")

# Load default settings (if available)
default_settings = {}
try:
    with open("default_settings.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.strip().split(": ")
            default_settings[key] = value
except FileNotFoundError:
    pass

# Create the drop-down lists
options = ["Option 1", "Option 2", "Option 3"]

dropdown1 = tk.StringVar()
dropdown1.set(default_settings.get("Option 1", options[0]))
dropdown1_menu = tk.OptionMenu(window, dropdown1, *options)
dropdown1_menu.config(width=20, height=2)  # Increase the width of the drop-down menu
dropdown1_menu.pack()

dropdown2 = tk.StringVar()
dropdown2.set(default_settings.get("Option 2", options[0]))
dropdown2_menu = tk.OptionMenu(window, dropdown2, *options)
dropdown2_menu.config(width=20, height=2)  # Increase the width of the drop-down menu
dropdown2_menu.pack()

dropdown3 = tk.StringVar()
dropdown3.set(default_settings.get("Option 3", options[0]))
dropdown3_menu = tk.OptionMenu(window, dropdown3, *options)
dropdown3_menu.config(width=20, height=2)  # Increase the width of the drop-down menu
dropdown3_menu.pack()

# Create the button to save settings
save_button = tk.Button(window, text="Save Settings", command=save_settings, width=15, height=2)
save_button.pack()

# Run the main event loop
window.mainloop()