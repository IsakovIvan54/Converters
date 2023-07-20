import tkinter as tk
import pyvisa

# Connect to the VISA backend
rm = pyvisa.ResourceManager()

# Get a list of available devic

def getIDN():
    devices = rm.list_resources()
    name_device = []
    name_visa = []
    for i in range(0,len(devices)):
        print("VISA: " + devices[i])
        name_visa.append(devices[i])
        instrument = rm.open_resource(devices[i])
        name_device.append(instrument.query('*IDN?'))
    return name_device, name_visa



temp_devices = getIDN()
dropdown_data = temp_devices[1]
device_name = temp_devices[0]

def save_changes():
    # Logic to save the changes made in the dropdown lists
    # This function will be called when the 'Save Changes' button is clicked
    for i, dropdown in enumerate(dropdowns):
        selected_value = dropdown.get()
        print(f"Dropdown {i+1} selected value: {selected_value}")

# Read dropdown data from the file
# with open('dropdown_data.txt', 'r') as file:
#     dropdown_data = file.read().splitlines()

# Create the GUI window
window = tk.Tk()
window.title("Dropdown Lists")
# window.geometry("300x200")

# Create a list to store the dropdowns
dropdowns = []

# Create dropdown lists based on the data read from the file
for i, data in enumerate(dropdown_data):
    label = tk.Label(window, text=device_name[i])
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