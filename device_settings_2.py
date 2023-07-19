import tkinter as tk

def save_changes():
    # Logic to save the changes made in the dropdown lists
    # This function will be called when the 'Save Changes' button is clicked
    for i, dropdown in enumerate(dropdowns):
        selected_value = dropdown.get()
        print(f"Dropdown {i+1} selected value: {selected_value}")

# Read dropdown data from the file
with open('dropdown_data.txt', 'r') as file:
    dropdown_data = file.read().splitlines()

# Create the GUI window
window = tk.Tk()
window.title("Dropdown Lists")
window.geometry("300x200")

# Create a list to store the dropdowns
dropdowns = []

# Create dropdown lists based on the data read from the file
for i, data in enumerate(dropdown_data):
    label = tk.Label(window, text=f"Dropdown {i+1}")
    label.pack()

    # Set the default value for each dropdown
    default_value = tk.StringVar(window)
    default_value.set(data.split(",")[0])  # Assuming the data in the file is comma-separated
    dropdown = tk.OptionMenu(window, default_value, *data.split(","))
    dropdown.pack()

    dropdowns.append(default_value)

# Create the 'Save Changes' button
save_button = tk.Button(window, text="Save Changes", command=save_changes)
save_button.pack()

# Start the GUI event loop
window.mainloop()