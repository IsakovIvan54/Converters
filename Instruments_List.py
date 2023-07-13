# import pyvisa

# # Initialize the pyvisa library
# rm = pyvisa.ResourceManager()

# # Get a list of all connected devices
# devices = rm.list_resources()

# # Iterate over each device and display its name and VISA resource
# for index, device in enumerate(devices):
#     try:
#         # Open the device
#         instrument = rm.open_resource(device)
        
#         # Get the name of the device
#         name = instrument.query('*IDN?')
        
#         # Display the name and VISA resource
#         print(f"Device {index+1}: {name.strip()}, VISA resource: {device}")
        
#         # Close the device
#         instrument.close()
#     except pyvisa.Error as e:
#         print(f"Error accessing device {index+1}: {e}")

# # Close the resource manager
# rm.close()

# import tkinter as tk
# from tkinter import messagebox
# import pyvisa

# def show_devices():
#     try:
#         # Initialize the pyvisa library
#         rm = pyvisa.ResourceManager()

#         # Get a list of all connected devices
#         devices = rm.list_resources()

#         # Display a pop-up list with the name and VISA resource of each device
#         messagebox.showinfo("Connected Devices", "\n".join(devices))

#         # Close the resource manager
#         rm.close()
#     except pyvisa.Error as e:
#         messagebox.showerror("Error", f"Error accessing devices: {e}")

# # Create the main window
# root = tk.Tk()
# root.title("Device List")

# # Create a button to show the connected devices
# show_devices_button = tk.Button(root, text="Show Devices", command=show_devices)
# show_devices_button.pack(padx=10, pady=10)

# # Run the main loop
# root.mainloop()

# import tkinter as tk
# from tkinter import messagebox, ttk
# import pyvisa

# def show_devices():
#     try:
#         # Initialize the pyvisa library
#         rm = pyvisa.ResourceManager()

#         # Get a list of all connected devices
#         devices = rm.list_resources()

#         # Display a pop-up list to select a device
#         root = tk.Tk()
#         root.title("Select Device")

#         device_var = tk.StringVar(root)
#         device_var.set(devices[0]) # Set the default selected device

#         device_label = tk.Label(root, text="Select a device:")
#         device_label.pack(padx=10, pady=10)

#         device_list = ttk.Combobox(root, textvariable=device_var, values=devices)
#         device_list.pack(padx=10, pady=5)

#         ok_button = tk.Button(root, text="OK", command=lambda: select_device(device_var.get()))
#         ok_button.pack(padx=10, pady=5)

#         root.mainloop()

#         # Close the resource manager
#         rm.close()
#     except pyvisa.Error as e:
#         messagebox.showerror("Error", f"Error accessing devices: {e}")

# def select_device(selected_device):
#     messagebox.showinfo("Selected Device", f"Selected device: {selected_device}")

# # Create the main window
# root = tk.Tk()
# root.title("Device List")

# # Create a button to show the connected devices
# show_devices_button = tk.Button(root, text="Show Devices", command=show_devices)
# show_devices_button.pack(padx=10, pady=10)

# # Run the main loop
# root.mainloop()

import pyvisa


rm = pyvisa.ResourceManager()
print(rm.list_resources())