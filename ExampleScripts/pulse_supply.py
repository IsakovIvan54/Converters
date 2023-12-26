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

SUPPLY600 = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
OSCILLOSCOPE = rm.open_resource('USB0::0x1AB1::0x0588::DS1ET244602180::INSTR') # Осциллограф 
# CONTROL_SUPPLY = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C244806702::INSTR') # Управляющий источник
# MULTIMETR = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O244701540::INSTR') # Мультиметр
LOAD = rm.open_resource('ASRL6::INSTR') # Электронная нагрузка

# # Настройка мультиметра
# MULTIMETR.write(':SENS:FUNC VOLT')
# MULTIMETR.write(':SENS:VOLTAGE:RANGE:AUTO ON')
# MULTIMETR.write(':SENS:VOLTAGE:NPLC 0.2')

# # Настройка источника для выключения 
# CONTROL_SUPPLY.write(':SOUR3:CURR 0.050')

# # Настройка осциллографа
# OSCILLOSCOPE.write(':CHAN1:DISP ON')  # Включение первого канала 
# OSCILLOSCOPE.write(':CHAN2:DISP OFF')  # Выключение второго канала
# OSCILLOSCOPE.write(':CHAN1:BWL ON') # Включение ограничения полосы
# OSCILLOSCOPE.write(':CHAN1:COUP AC')  # Установка AC
# OSCILLOSCOPE.write(':CHAN1:OFFS 0')  # Установка смещения
# OSCILLOSCOPE.write(':CHAN1:PROB 1')  # Установка 1x ослабления
# OSCILLOSCOPE.write(':CHAN1:SCAL 0.1') # Установка 100 мВ на клетку
# OSCILLOSCOPE.write(':TIM:SCAL 0.000002') # Установка 2 мкс на клетку
# OSCILLOSCOPE.write(':TRIG:EDGE:LEV 0.07 ') # Установка тригера 70 мВ

# Настройка нагрузки
LOAD.write('SYST:REM')
LOAD.write('FUNC CURR')
co = 0
timeB = 0.1

LOAD.write('CURR ' + str(12.5))
LOAD.write(':INP ON')

SUPPLY600.write('SOUR:VOLT ' + str(180))
SUPPLY600.write(':OUTP ON')

while co <= 10:
    SUPPLY600.write('SOUR:VOLT ' + str(180))
    time.sleep(timeB)
    SUPPLY600.write('SOUR:VOLT ' + str(375))
    time.sleep(timeB)
    co +=1

SUPPLY600.write(':OUTP OFF')
LOAD.write(':INP OFF')