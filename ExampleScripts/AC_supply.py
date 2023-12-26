import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np
from PIL import Image, ImageTk
from tkinter import Tk, Radiobutton, StringVar


version = 'Версия: 1.1.7'
rm = pyvisa.ResourceManager()
pygame.mixer.init()
print(rm.list_resources())

SUPPLY = rm.open_resource('ASRL8::INSTR') # Источник AC
print(SUPPLY.query('*IDN?'))


# SUPPLY.write(':CURR:LIM:PEAK:HIGH')
SUPPLY.write(':MODE AC-INT')
SUPPLY.write(':FREQ 50')
SUPPLY.write(':VOLT:RANG 200')


SUPPLY.write(':VOLT '+str(10))



# SUPPLY.write('SYST:REM')
# SUPPLY.write('SOUR:CURR' + str(1))

# SUPPLY.write('SOUR:VOLT' + str(1))



SUPPLY.write(':OUTP ON')

time.sleep(2)
print(SUPPLY.query(':MEAS:VOLT:RMS?'))
print(SUPPLY.query(':MEAS:CURR:RMS?'))
print(SUPPLY.query(':MEAS:POW:PFAC?'))
SUPPLY.write(':OUTP OFF')
