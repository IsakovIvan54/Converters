import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np


dateString = 'TESTS'
# dateString = time.strftime("%Y-%m-%d_%H%M")
filepath = "./" + dateString + ".csv"

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

# Настройка источника для выключения 
RIG_DL831A.write(':SOUR1:CURR 0.050')


# # Настройка осциллографа
# RIG_MSO8104.write(':CHAN1:DISP ON')  # enable channel 1 display
# RIG_MSO8104.write(':CHAN1:COUP AC ')  # DC coupling
# RIG_MSO8104.write(':CHAN1:IMP OMEG')  # 1 MOhm input impedance
# RIG_MSO8104.write(':CHAN1:PROBE 1')  # 1x probe attenuation
# RIG_MSO8104.write(':CHAN1:BWL 20M')
# RIG_MSO8104.write(':CHAN1:SCAL 0.1')
# RIG_MSO8104.write(':TIM:SCAL 0.000002')

INVOLT =300
OUTCURR = 8.93
DVolt = 5
# value = [1,2]


nominal_output_voltage = 28

intervals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
value = [0, 0, 0, 0, 0, 0, 0]

time.sleep(1)
AKIP.write('SOUR:VOLT ' + str(INVOLT))
RIG_DL3031A.write('CURR ' + str(OUTCURR))

AKIP.write(':OUTP ON')

time.sleep(1)

RIG_DL3031A.write(':INP ON')
RIG_DL831A.write('OUTP CH1, ON')
RIG_DL831A.write(f':SOUR1:VOLT {DVolt}')

time.sleep(1)


VoltOut = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))


while VoltOut <= intervals[6]*nominal_output_voltage  :
    VoltOut = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))
    print ('Напряжение регулировки: ' + str(VoltOut))
    if VoltOut <= 0.1*nominal_output_voltage:
        value[0] = VoltOut
    elif (VoltOut > 0.1*nominal_output_voltage) & (VoltOut <= 0.2*nominal_output_voltage):
        value[1] = VoltOut
    elif (VoltOut > 0.2*nominal_output_voltage) & (VoltOut <= 0.3*nominal_output_voltage):
        value[2] = VoltOut
    elif (VoltOut > 0.3*nominal_output_voltage) & (VoltOut <= 0.4*nominal_output_voltage):
        value[3] = VoltOut
    elif (VoltOut > 0.4*nominal_output_voltage) & (VoltOut <= 0.5*nominal_output_voltage):
        value[4] = VoltOut
    elif (VoltOut > 0.5*nominal_output_voltage) & (VoltOut <= 0.6*nominal_output_voltage):
        value[5] = VoltOut
    elif (VoltOut > 0.6*nominal_output_voltage) & (VoltOut <= 0.7*nominal_output_voltage):
        value[6] = VoltOut
    
print(value)

RIG_DL831A.write('OUTP CH1, OFF')
AKIP.write(':OUTP OFF')
RIG_DL3031A.write(':INP OFF')
