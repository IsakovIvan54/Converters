import pyvisa

# Connect to the VISA backend
rm = pyvisa.ResourceManager()

# Get a list of available devices
devices = rm.list_resources()

# Create objects for each device
device_objects = {}
for device in devices:
    # Open the device
    instrument = rm.open_resource(device)
    
    # Send the *IDN? command to get the device name
    name = instrument.query('*IDN?')
    
    # Store the device object with its corresponding name
    device_objects[name.strip()] = instrument

# Example usage:
# Access the device object by its name
device_name = "DeviceName"
if device_name in device_objects:
    device = device_objects[device_name]
    # Do something with the device object
    device.write('Some SCPI command')
else:
    print(f"Device '{device_name}' not found")

# Close all device connections
for device in device_objects.values():
    device.close()