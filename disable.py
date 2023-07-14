import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
import pygame


import numpy as np
rm = pyvisa.ResourceManager()

pygame.mixer.init()
print(rm.list_resources())

rm = pyvisa.ResourceManager()
RIG_DL3031A = rm.open_resource('USB0::0x1AB1::0x0E11::DL3D244200321::INSTR')
AKIP = rm.open_resource('TCPIP0::192.168.0.175::HISLIP0::INSTR')
KEITHDMM6500 = rm.open_resource('USB0::0x05E6::0x6500::04530036::INSTR')

RIG_DL831A = rm.open_resource('USB0::0x1AB1::0x0E11::DP8A244400389::INSTR')
# RIG_MSO8104 = rm.open_resource('USB0::0x1AB1::0x0516::DS8A242800498')


# Настройка источника
AKIP.write('SOUR:CURR 1.3')

# Настройка мультиметра
KEITHDMM6500.write(':SENSE:FUNCTION "VOLT"')
KEITHDMM6500.write(':SENSE:VOLTAGE:RANGE:AUTO ON')

# Настройка нагрузки
RIG_DL3031A.write('INST OUT1')
RIG_DL3031A.write('SOUR:CURR:SLEW 0.5')
RIG_DL3031A.write(':SOUR:CURR:RANG 60')


print(RIG_DL831A.query('*IDN?'))

                
voltage = 2.0  # Replace with the desired voltage in volts
RIG_DL831A.write(':SOUR1:CURR 0.050')
RIG_DL831A.write('OUTP CH1, ON')

for i in np.arange(0,5,0.5):
    
    RIG_DL831A.write(f':SOUR1:VOLT {i}')
    time.sleep(0.8)
    voltage1 = float(RIG_DL831A.query('MEAS:VOLT? CH1'))
    print(voltage1)
    if 2.4 <= voltage1 <= 2.6:
        break
    
RIG_DL831A.write('OUTP CH1, OFF')



def run_script():

    voltage = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))
    print(voltage)

def exit_window():
    root.destroy()


root = tk.Tk()

root.geometry('760x220')

run_button = tk.Button(root, text='Run', command=run_script)
run_button.grid(row=6, column=2)

exit_button = tk.Button(root, text='Exit', command=exit_window)
exit_button.grid(row=6, column=3)

# root.mainloop()