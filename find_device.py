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


devices = getIDN()
for i in range(0,len(devices[0])):
    print(devices[0][i])
