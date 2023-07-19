import pyvisa

# Connect to the VISA backend
rm = pyvisa.ResourceManager()

# Get a list of available devices
devices = rm.list_resources()



print(devices)
print("Количество подключенных приборов:" + str(len(devices)))
print(devices[0])

device_objects = {}

for i in range(0,len(devices)):
    print("VISA: " + str(devices[i]))
    instrument = rm.open_resource(devices[i])
    print(instrument.query('*IDN?'))