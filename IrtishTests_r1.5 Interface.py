import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np
from PIL import Image, ImageTk
from tkinter import Tk, Radiobutton, StringVar


version = 'Версия: 1.1.5'
# rm = pyvisa.ResourceManager()
# pygame.mixer.init()
# print(rm.list_resources())

# # SUPPLY600 = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
# # SUPPLY150 = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
# OSCILLOSCOPE = rm.open_resource('USB0::0x1AB1::0x0588::DS1ET244602180::INSTR') # Осциллограф 
# CONTROL_SUPPLY = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C244806702::INSTR') # Управляющий источник
# MULTIMETR = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O244701540::INSTR') # Мультиметр
# LOAD = rm.open_resource('ASRL7::INSTR') # Электронная нагрузка

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

# # Настройка нагрузки
# LOAD.write('SYST:REM')
# LOAD.write('FUNC CURR')

def chose_dev150():
    print("Выбран источник 150В")
    
def chose_dev600():
    print("Выбран источник 600В")

# # Функции кнопок
# def reg_Down(INVOLT, OUTCURR, DVolt, nominal_output_voltage): # Крутить с крайнего правого положения в левое
#     if selection.get() == 'USB0::0x2EC7::0x6700::805033011787020025::INSTR':
#         SUPPLY = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
#         SUPPLY.write('SOUR:CURR 10')
#     elif selection.get() == 'USB0::0xFFFF::0x6500::805037011786920001::INSTR':
#         SUPPLY = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
#         SUPPLY.write('SOUR:CURR 30')


#     dateString_reg_down =  NameConverter.get() + 'Reg_down'
#     filepath_reg_down = "./" + dateString_reg_down + ".csv"
    
#     intervals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
#     value = [0, 0, 0, 0, 0, 0, 0]

#     time.sleep(1)
#     SUPPLY.write('SOUR:VOLT ' + str(INVOLT))
#     LOAD.write('CURR ' + str(OUTCURR))
#     SUPPLY.write(':OUTP ON')
#     time.sleep(1)
#     LOAD.write(':INP ON')
#     CONTROL_SUPPLY.write('OUTP CH3, ON')
#     CONTROL_SUPPLY.write(f':SOUR3:VOLT {DVolt}')
#     time.sleep(1)
#     VoltOut = float(MULTIMETR.query(':MEAS:VOLT:DC?'))

#     while VoltOut <= intervals[6]*nominal_output_voltage  :
#         VoltOut = float(MULTIMETR.query(':MEAS:VOLT:DC?'))
#         print ('Напряжение регулировки: ' + str(VoltOut))
#         if VoltOut <= 0.1*nominal_output_voltage:
#             value[0] = VoltOut
#         elif (VoltOut > 0.1*nominal_output_voltage) & (VoltOut <= 0.2*nominal_output_voltage):
#             value[1] = VoltOut
#         elif (VoltOut > 0.2*nominal_output_voltage) & (VoltOut <= 0.3*nominal_output_voltage):
#             value[2] = VoltOut
#         elif (VoltOut > 0.3*nominal_output_voltage) & (VoltOut <= 0.4*nominal_output_voltage):
#             value[3] = VoltOut
#         elif (VoltOut > 0.4*nominal_output_voltage) & (VoltOut <= 0.5*nominal_output_voltage):
#             value[4] = VoltOut
#         elif (VoltOut > 0.5*nominal_output_voltage) & (VoltOut <= 0.6*nominal_output_voltage):
#             value[5] = VoltOut
#         elif (VoltOut > 0.6*nominal_output_voltage) & (VoltOut <= 0.7*nominal_output_voltage):
#             value[6] = VoltOut 
#     print(value)

#     CONTROL_SUPPLY.write('OUTP CH3, OFF')
#     SUPPLY.write(':OUTP OFF')
#     LOAD.write(':INP OFF')

#     with open(filepath_reg_down, "a") as file:
#         if os.stat(filepath_reg_down).st_size == 0: #if empty file, write a nice header
#             file.write("Регулировка" + str(intervals[0]) + " От номинального [V];" + "Регулировка" + str(intervals[1]) + " От номинального [V];" + "Регулировка" + str(intervals[2]) + " От номинального [V];" + "Регулировка" + str(intervals[3]) + " От номинального [V]; "+"Регулировка" + str(intervals[4]) + " От номинального [V];"+ "Регулировка" + str(intervals[5]) + " От номинального [V];" + "Регулировка" + str(intervals[6]) + " От номинального [V];" +"\n")
#         file.write("{};{};{};{};{};{};{};\n".format(value[0], value[1], value[2], value[3], value[4], value[5], value[6])) # log the data
#     file.close()

#     pygame.mixer.music.load('sound.wav')
#     pygame.mixer.music.play(0)
#     return value

# def reg_Up(INVOLT, OUTCURR, DVolt, nominal_output_voltage): # Крутить с крайнего правого положения в левое
    if selection.get() == 'USB0::0x2EC7::0x6700::805033011787020025::INSTR':
        SUPPLY = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
        SUPPLY.write('SOUR:CURR 10')
    elif selection.get() == 'USB0::0xFFFF::0x6500::805037011786920001::INSTR':
        SUPPLY = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
        SUPPLY.write('SOUR:CURR 30')
   
    dateString_reg_up = NameConverter.get() + 'Reg_up'
    filepath_reg_up = "./" + dateString_reg_up + ".csv"

    intervals = [1.05, 1.1]
    value = [0, 0]

    time.sleep(1)
    SUPPLY.write('SOUR:VOLT ' + str(INVOLT))
    LOAD.write('CURR ' + str(OUTCURR))
    SUPPLY.write(':OUTP ON')
    time.sleep(1)
    LOAD.write(':INP ON')
    CONTROL_SUPPLY.write('OUTP CH3, ON')
    CONTROL_SUPPLY.write(f':SOUR3:VOLT {DVolt}')
    time.sleep(1)
    VoltOut = float(MULTIMETR.query(':MEAS:VOLT:DC?'))

    while VoltOut <= intervals[1]*nominal_output_voltage  :
        VoltOut = float(MULTIMETR.query(':MEAS:VOLT:DC?'))
        print ('Напряжение регулировки: ' + str(VoltOut))
        if VoltOut <= 1.05*nominal_output_voltage:
            value[0] = VoltOut
        elif (VoltOut > 1.05*nominal_output_voltage) & (VoltOut <= 1.1*nominal_output_voltage):
            value[1] = VoltOut 
    print(value)

    CONTROL_SUPPLY.write('OUTP CH3, OFF')
    SUPPLY.write(':OUTP OFF')
    LOAD.write(':INP OFF')

    with open(filepath_reg_up, "a") as file:
        if os.stat(filepath_reg_up).st_size == 0: #if empty file, write a nice header
            file.write("Регулировка" + str(intervals[0]) + " От номинального [V];" + "Регулировка" + str(intervals[1]) +"\n")
        file.write("{};{};\n".format(value[0], value[1])) # log the data
    file.close()

    pygame.mixer.music.load('sound.wav')
    pygame.mixer.music.play(0)
    return value

def issue_prot():
    print('Протокол выпущен!')

def reg_Down_But():
    VolInNom = int(InPutV2.get())
    IoutNom = float(OutCurr.get())
    nominal_output_voltage = float(NomOutVolt.get())
    disable_volt = float(DisVolt.get())
    reg_Down_list = reg_Down(VolInNom, IoutNom, disable_volt, nominal_output_voltage)
    print('Регулировка выходного напряжения:' + str(reg_Down_list))

def reg_Up_But():
    VolInNom = int(InPutV2.get())
    IoutNom = float(OutCurr.get())
    nominal_output_voltage = float(NomOutVolt.get())
    disable_volt = float(DisVolt.get())
    reg_Up_list = reg_Up(VolInNom, IoutNom, disable_volt, nominal_output_voltage)
    print('Регулировка выходного напряжения:' + str(reg_Up_list))

def exit_window():
    root.destroy()

# def run_TEST(INVOLT, OUTCURR, DVolt):
#     if selection.get() == 'USB0::0x2EC7::0x6700::805033011787020025::INSTR':
#         SUPPLY = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
#         SUPPLY.write('SOUR:CURR 10')
#     elif selection.get() == 'USB0::0xFFFF::0x6500::805037011786920001::INSTR':
#         SUPPLY = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
#         SUPPLY.write('SOUR:CURR 30')

#     time.sleep(1)
#     SUPPLY.write('SOUR:VOLT ' + str(INVOLT))
#     LOAD.write('CURR ' + str(OUTCURR))
#     CONTROL_SUPPLY.write(f':SOUR3:VOLT {DVolt}')
#     SUPPLY.write(':OUTP ON')
#     CONTROL_SUPPLY.write('OUTP CH3, ON')
#     time.sleep(1)
#     currentHH = float(SUPPLY.query('MEAS:CURR?')) # Входный ток без нагрузки
#     voltageHH = float(SUPPLY.query('MEAS:VOLT?')) # Входное напряжение без нагрузки
#     time.sleep(2)
#     voltageHHout = float(MULTIMETR.query(':MEAS:VOLT:DC?')) # Выходное напряжение без нагрузки
#     time.sleep(0.2)
#     LOAD.write(':INP ON')
#     time.sleep(3)
#     currentLOAD = float(SUPPLY.query('MEAS:CURR?')) # Входный ток c нагрузкой
#     voltageLOAD = float(SUPPLY.query('MEAS:VOLT?')) # Входное напряжение c нагрузкой
#     voltageLOADout = float(MULTIMETR.query(':MEAS:VOLT:DC?')) # Выходное напряжение  c нагрузкой
#     currentLOADout = float(LOAD.query('MEAS:CURR?')) # Выходной ток c нагрузкой
#     Noise = float(OSCILLOSCOPE.query(':MEAS:VRMS? CHAN1')) * 1000
#     NoisePP = float(OSCILLOSCOPE.query(':MEAS:VPP? CHAN1')) * 1000
#     kpd = ((voltageLOADout * currentLOADout) / (currentLOAD * voltageLOAD)) * 100
#     LOAD.write(':INP OFF')
#     SUPPLY.write(':OUTP OFF')
#     CONTROL_SUPPLY.write('OUTP CH3, OFF')
#     print('------------------------------------------------------------------------')
#     print(f'Напряжение ХХ: {voltageHHout:.3f}')
#     print(f'Входной ток ХХ: {currentHH:.3f} A, Входное напряжение ХХ: {voltageHH:.3f} V')
#     print(f'Напряжение под нагрузкой: {voltageLOADout:.3f} V, Ток под нагрузкой: {currentLOADout:.3f} A')
#     print(f'Входной ток под нагрузкой: {currentLOAD:.3f} A, Входное напряжение под нагрузкой: {voltageLOAD:.3f} V')
#     print(f'КПД: {kpd:.1f} %')
#     print(f'Пульсации Vrms: {Noise:.1f} mV')
#     print(f'Пульсации Vp-p: {NoisePP:.1f} mV')
#     return[voltageHHout, voltageLOADout, kpd, Noise, NoisePP]

# def Disable_Volt(INVOLT, OUTCURR, DVolt, nominal_output_voltage):
#     if selection.get() == 'USB0::0x2EC7::0x6700::805033011787020025::INSTR':
#         SUPPLY = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
#         SUPPLY.write('SOUR:CURR 10')
#     elif selection.get() == 'USB0::0xFFFF::0x6500::805037011786920001::INSTR':
#         SUPPLY = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
#         SUPPLY.write('SOUR:CURR 30')

#     time.sleep(1)
#     SUPPLY.write('SOUR:VOLT ' + str(INVOLT))
#     LOAD.write('CURR ' + str(OUTCURR))
#     SUPPLY.write(':OUTP ON')
#     time.sleep(1)
#     LOAD.write(':INP ON')
#     CONTROL_SUPPLY.write('OUTP CH3, ON')
#     CONTROL_SUPPLY.write(f':SOUR3:VOLT {DVolt}')
#     time.sleep(1)

#     for VoltageDis in np.arange(DVolt,0,-0.05):
        
#         CONTROL_SUPPLY.write(f':SOUR3:VOLT {VoltageDis}')
#         time.sleep(0.1)
#         voltageOUT = float(MULTIMETR.query(':MEAS:VOLT:DC?'))
        
#         if voltageOUT <= nominal_output_voltage/2:
#             break
#     CONTROL_SUPPLY.write('OUTP CH3, OFF')
#     LOAD.write(':INP OFF')
#     SUPPLY.write(':OUTP OFF')
#     print("Напряжение отключения [V]" + str(VoltageDis))
#     return VoltageDis

# def Disable_Volt_NOLOAD(INVOLT, DVolt, nominal_output_voltage):
    if selection.get() == 'USB0::0x2EC7::0x6700::805033011787020025::INSTR':
        SUPPLY = rm.open_resource('USB0::0x2EC7::0x6700::805033011787020025::INSTR') # Источник 600В
        SUPPLY.write('SOUR:CURR 10')
    elif selection.get() == 'USB0::0xFFFF::0x6500::805037011786920001::INSTR':
        SUPPLY = rm.open_resource('USB0::0xFFFF::0x6500::805037011786920001::INSTR') # Источник 150В
        SUPPLY.write('SOUR:CURR 30')

    time.sleep(1)
    SUPPLY.write('SOUR:VOLT ' + str(INVOLT))
    SUPPLY.write(':OUTP ON')
    time.sleep(1)
    CONTROL_SUPPLY.write(f':SOUR3:VOLT {DVolt}')
    CONTROL_SUPPLY.write('OUTP CH3, ON')
    time.sleep(1)

    for VoltageDis in np.arange(DVolt,0,-0.05):
        CONTROL_SUPPLY.write(f':SOUR3:VOLT {VoltageDis}')
        time.sleep(0.1)
        voltageOUT = float(MULTIMETR.query(':MEAS:VOLT:DC?'))
        print(voltageOUT)
        if voltageOUT <= nominal_output_voltage*0.99:
            break
    CONTROL_SUPPLY.write('OUTP CH3, OFF')
    SUPPLY.write(':OUTP OFF')
    return VoltageDis

def run_script():

    dateString = NameConverter.get()
    filepath = "./" + dateString + ".csv"

    VolInMin = int(InPutV1.get())
    VolInNom = int(InPutV2.get())
    VolInMax = int(InPutV3.get())
    IoutNom = float(OutCurr.get())
    IoutNomH = float(OutCurr.get())/2

    accur_output_voltage = float(АcOutVolt.get())
    nominal_output_voltage = float(NomOutVolt.get())
    max_line_reg = float(MaxLineReg.get())
    max_load_reg = float(MaxLoadReg.get())
    max_riple_abs = float(MaxRipple.get())
    disable_volt = float(DisVolt.get())
    disable_volt_max = float(DisVoltMax.get())
    disable_volt_min = float(DisVoltMin.get())
    
    valueMin = run_TEST(VolInMin, IoutNom, disable_volt)
    valueNom = run_TEST(VolInNom, IoutNom, disable_volt)
    valueMax = run_TEST(VolInMax, IoutNom, disable_volt)

    valueHalf = run_TEST(VolInNom, IoutNomH, disable_volt)

    DisableVoltage = round(Disable_Volt(VolInNom, IoutNom, disable_volt, nominal_output_voltage),3)
    # DisableVoltageMax = Disable_Volt(VolInNom, disable_volt, nominal_output_voltage)

    VoutNoLoadNOM = round(valueNom[0], 3)
    VoutLoadMin = round(valueMin[1], 3)
    VoutLoadNom = round(valueNom[1], 3)
    VoutLoadMax = round(valueMax[1], 3)

    VoutLoadNomHalf = round(valueHalf[1], 3)

    LineRegLow = round((VoutLoadNom - VoutLoadMin) / VoutLoadNom * 100, 3)
    LineRegHigh = round((VoutLoadNom - VoutLoadMax) / VoutLoadNom * 100, 3)
    if LineRegLow <= 0:
        LineRegLow = -1*LineRegLow
    if LineRegHigh <= 0:
        LineRegHigh = -1*LineRegHigh

    LineReg = max(LineRegLow, LineRegHigh)
    
    LoadReg = round((VoutLoadNom - VoutNoLoadNOM) / VoutLoadNom * 100, 3)
    if LoadReg <= 0:
        LoadReg = -1*LoadReg

    RiplePP = round(valueNom[4],1)
    RipleRMS = round(valueNom[3],1)

    KPDMin = round(valueMin[2],1)
    KPDNom = round(valueNom[2],1)
    KPDMax = round(valueMax[2],1)

    output_text1.set('Выходное напряжение [В]: ' + str(VoutLoadNom))
    output_text2.set('Load regulation [%]: ' + str(LoadReg))
    output_text3.set('Line regulation [%]: ' + str(LineReg))
    output_text4.set('КПД [%]: ' + str(KPDNom)),
    output_text5.set('Пульсации  [мВ p-p]: ' + str(RiplePP))
    output_text6.set('Напряжение отключения [В]: ' + str(DisableVoltage))

    if (nominal_output_voltage - nominal_output_voltage*accur_output_voltage/100) <= VoutLoadNom <= (nominal_output_voltage + nominal_output_voltage*accur_output_voltage/100):
        output_label1.config(fg="green")
    else: 
        output_label1.config(fg="red")

    if (LineReg <= max_line_reg):
        output_label3.config(fg="green")
    else: 
        output_label3.config(fg="red")

    if (LoadReg <= max_load_reg):
        output_label2.config(fg="green")
    else: 
        output_label2.config(fg="red")

    if (RiplePP <= max_riple_abs):
        output_label5.config(fg="green")
    else: 
        output_label5.config(fg="red")
    if (disable_volt_min <= DisableVoltage <= disable_volt_max):
        output_label6.config(fg="green")
    else: 
        output_label6.config(fg="red")

    # Write results to a file
    with open(filepath, "a") as file:
        if os.stat(filepath).st_size == 0: #if empty file, write a nice header
            file.write("Выходное напряжение (без нагрузки) [V];" + 
                        "Выходное напряжение при Vin" + str(VolInMin) + " [V];" + 
                        "Выходное напряжение при Vin" + str(VolInNom)+ " [V];" + 
                        "Выходное напряжение при Vin" + str(VolInMax)+ " [V];" + 
                        "LineReg [%];"+ 
                        "LoadReg [%];"+
                        "Пульсации [мВp-p];"+
                        "ПульсацииRMS [мВ];" + 
                        "КПД при Vin" + str(VolInMin) + " [V];" + 
                        "КПД при Vin" + str(VolInNom)+ " [V];" + 
                        "КПД при Vin" + str(VolInMax)+ " [V];" + 
                        "Напряжение отключения [V];" + 
                        "Выходное напряжение(половина нагрузки) при Vin" + str(VolInNom)+ " [V];" +
                        "\n")
        file.write("{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(VoutNoLoadNOM, VoutLoadMin, VoutLoadNom, VoutLoadMax, LineReg, LoadReg,RiplePP, RipleRMS, KPDMin, KPDNom, KPDMax, DisableVoltage,VoutLoadNomHalf)) # log the data
    file.close()

    pygame.mixer.music.load('sound.wav')
    pygame.mixer.music.play(0) 

w_column = 5
1.8
root = tk.Tk()
root.title('ПО для проверки DC-DC преобразователей серии "Иртыш"')
# root.geometry("1130x600")
# root.geometry("1695x900")
# root.geometry("1808x960")
root.geometry("1920x1080")
# root.attributes('-fullscreen',True)


# Описание шапки
tk.Label(root, text='Проверка DC-DC преобразователей серии "Иртыш"', font="Verdana 24 normal").place(x=460, y=0)

tk.Label(root, text='Наименование преобразователя:', font="Verdana 30 normal").place(x=430, y=40)
NameConverter = tk.Entry(root,font=("Arial", 30))
NameConverter.place(x=1130, y=45)

# Добавление версии программы
tk.Label(root, text=version, font="Verdana 8 normal").place(x=0, y=990)



# Добавление логотипа
label_image1 = Image.open("EKBlogoNew.png")
img=label_image1.resize((95, 70))
label_image = ImageTk.PhotoImage(img)
tk.Label(root, image=label_image).place(x=1800, y=920)


# Создание фреймов
input_frame = tk.LabelFrame(root, text="Параметры преобразователя", font=("Arial", 24))
input_frame.pack(padx=10, pady=10, ipadx=10, ipady=10)
input_frame.place(x=10, y=110,width = 1900)

button_frame = tk.LabelFrame(root, text="Меню", font=("Arial", 24))
button_frame.pack(padx=5, pady=5)
button_frame.place(x=95, y=750)

output_frame = tk.LabelFrame(root, text="Измеренные параметры преобразователя", font=("Arial", 24))
output_frame.pack(padx=10, pady=10,ipadx=600, ipady=555)
output_frame.place(x=10, y=530,width = 1900)

suplly_frame = tk.LabelFrame(root, text="Выбор источника питания", font=("Arial", 24))
suplly_frame.pack(padx=10, pady=10, ipadx=10, ipady=10)
suplly_frame.place(x=10, y=0)


# Настройка выбора источника 
selection = StringVar(value="USB0::0xFFFF::0x6500::805037011786920001::INSTR")
radio_button_1 = Radiobutton(suplly_frame, text="Источник 150В", variable=selection, value="USB0::0xFFFF::0x6500::805037011786920001::INSTR", command=chose_dev150,font="Verdana 14 normal")
radio_button_2 = Radiobutton(suplly_frame, text="Источник 600В", variable=selection, value="USB0::0x2EC7::0x6700::805033011787020025::INSTR", command=chose_dev600,font="Verdana 14 normal")
radio_button_1.grid(row=0, column=0,  ipadx=6, ipady=7)
radio_button_2.grid(row=0, column=1,  ipadx=6, ipady=7)

# Параметры преобразователя
tk.Label(input_frame, text='Минимальное входное напряжение[В]:', font="Verdana 24 normal").grid(row=0, column=0)
InPutV1 = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
InPutV1.grid(row=0, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальное входное напряжение[В]:', font="Verdana 24 normal").grid(row=1, column=0)
InPutV2 = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
InPutV2.grid(row=1, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Максимальное входное напряжение[В]:', font="Verdana 24 normal").grid(row=2, column=0)
InPutV3 = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
InPutV3.grid(row=2, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Ток нагрузки[А]:', font="Verdana 24 normal").grid(row=3, column=0)
OutCurr = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
OutCurr.grid(row=3, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальное выходное напряжение[В]:', font="Verdana 24 normal").grid(row=4, column=0)
NomOutVolt = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
NomOutVolt.grid(row=4, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Начальное напряжение на управляющем входе[В]:', font="Verdana 24 normal").grid(row=5, column=0)
DisVolt = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
DisVolt.grid(row=5, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Отклонение выходного напряжения[%]:', font="Verdana 24 normal").grid(row=0, column=2)
АcOutVolt = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
АcOutVolt.grid(row=0, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Load regulation max[%]:', font="Verdana 24 normal").grid(row=1, column=2)
MaxLoadReg = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
MaxLoadReg.grid(row=1, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Line regulation max[%]:', font="Verdana 24 normal").grid(row=2, column=2)
MaxLineReg = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
MaxLineReg.grid(row=2, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальный КПД[%]:', font="Verdana 24 normal").grid(row=3, column=2)
NominalKpd = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
NominalKpd.grid(row=3, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text= 'Максимальные пульсации[мВ]:', font="Verdana 24 normal").grid(row=4, column=2)
MaxRipple = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
MaxRipple.grid(row=4, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Минимальное управляющее напряжение[В]:', font="Verdana 24 normal").grid(row=5, column=2)
DisVoltMin = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
DisVoltMin.grid(row=5, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Максимальное управляющее напряжение[В]:', font="Verdana 24 normal").grid(row=6, column=2)
DisVoltMax = tk.Entry(input_frame,font=("Arial", 24),width=w_column)
DisVoltMax.grid(row=6, column=3,  ipadx=6, ipady=7)



# Меню
run_button = tk.Button(button_frame, text='Запуск проверки', command=run_script, font="Verdana 24 normal",compound='center',wraplength=200)
run_button.config(width=15, height=2)
run_button.grid(row=0, column=0,padx=5,pady=5)

reg_down_button = tk.Button(button_frame, text='Регулировка вниз', command=reg_Down_But, font="Verdana 24 normal",compound='center',wraplength=220)
reg_down_button.config(width=15, height=2)
reg_down_button.grid(row=0, column=1,padx=5,pady=5)

reg_down_button = tk.Button(button_frame, text='Регулировка вверх', command=reg_Up_But, font="Verdana 24 normal",compound='center',wraplength=220)
reg_down_button.config(width=15, height=2)
reg_down_button.grid(row=0, column=2,padx=5,pady=5)

protocol_button = tk.Button(button_frame, text='Выпустить протокол', command=issue_prot, font="Verdana 24 normal",compound='center',wraplength=200)
protocol_button.config(width=15, height=2)
protocol_button.grid(row=0, column=3,padx=5,pady=5)

exit_button = tk.Button(button_frame, text='Выход', command=exit_window, font="Verdana 24 normal",compound='center')
exit_button.config(width=15, height=2)
exit_button.grid(row=0, column=4,padx=5,pady=5)

# Измеренные параметры
output_text1 = tk.StringVar(value='Выходное напряжение [В]: ')
output_label1 = tk.Label(output_frame, textvariable=output_text1, font="Verdana 24 normal")
output_label1.grid(row=0, column=1)

output_textout1 = tk.StringVar()
output_labelout1 = tk.Label(output_frame, textvariable=output_textout1, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout1.grid(row=0, column=3,  ipadx=6, ipady=7)

output_text2 = tk.StringVar(value='Load regulation [%]: ')
output_label2 = tk.Label(output_frame, textvariable=output_text2, font="Verdana 24 normal")
output_label2.grid(row=1, column=1)

output_textout2 = tk.StringVar()
output_labelout2 = tk.Label(output_frame, textvariable=output_textout2, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout2.grid(row=1, column=3,  ipadx=6, ipady=7)

output_text3 = tk.StringVar(value='Line regulation [%]: ')
output_label3 = tk.Label(output_frame, textvariable=output_text3, font="Verdana 24 normal")
output_label3.grid(row=2, column=1)

output_textout3 = tk.StringVar()
output_labelout3 = tk.Label(output_frame, textvariable=output_textout3, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout3.grid(row=2, column=3,  ipadx=6, ipady=7)

output_text4 = tk.StringVar(value='КПД [%]: ')
output_label4 = tk.Label(output_frame, textvariable=output_text4, font="Verdana 24 normal")
output_label4.grid(row=0, column=5)

output_textout4 = tk.StringVar()
output_labelout4 = tk.Label(output_frame, textvariable=output_textout4, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout4.grid(row=0, column=7,  ipadx=6, ipady=7)

output_text5 = tk.StringVar(value='Пульсации  [мВ p-p]: ')
output_label5 = tk.Label(output_frame, textvariable=output_text5, font="Verdana 24 normal")
output_label5.grid(row=1, column=5)

output_textout5 = tk.StringVar()
output_labelout5 = tk.Label(output_frame, textvariable=output_textout5, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout5.grid(row=1, column=7,  ipadx=6, ipady=7)

output_text6 = tk.StringVar(value='Напряжение отключения [В]: ')
output_label6 = tk.Label(output_frame, textvariable=output_text6, font="Verdana 24 normal")
output_label6.grid(row=2, column=5)

output_textout6 = tk.StringVar()
output_labelout6 = tk.Label(output_frame, textvariable=output_textout6, font="Verdana 24 normal",background='white',width=w_column,relief='sunken')
output_labelout6.grid(row=2, column=7,  ipadx=6, ipady=7)

labelNULL0 = tk.StringVar(value='                           ')
labelNULL1 = tk.StringVar(value='                          ')
labelNULL2 = tk.StringVar(value='                         ')
labelNULL3 = tk.StringVar(value='         ')


output_labelNULL0 = tk.Label(output_frame, textvariable=labelNULL0, font="Verdana 14 normal")
output_labelNULL0.grid(row=0, column=0) 

output_labelNULL0 = tk.Label(output_frame, textvariable=labelNULL0, font="Verdana 14 normal")
output_labelNULL0.grid(row=1, column=0)

output_labelNULL0 = tk.Label(output_frame, textvariable=labelNULL0, font="Verdana 14 normal")
output_labelNULL0.grid(row=2, column=0)

output_labelNULL1 = tk.Label(output_frame, textvariable=labelNULL1, font="Verdana 14 normal")
output_labelNULL1.grid(row=0, column=2)

output_labelNULL1 = tk.Label(output_frame, textvariable=labelNULL1, font="Verdana 14 normal")
output_labelNULL1.grid(row=1, column=2)

output_labelNULL1 = tk.Label(output_frame, textvariable=labelNULL1, font="Verdana 14 normal")
output_labelNULL1.grid(row=2, column=2)

output_labelNULL2 = tk.Label(output_frame, textvariable=labelNULL2, font="Verdana 14 normal")
output_labelNULL2.grid(row=0, column=4)

output_labelNULL2 = tk.Label(output_frame, textvariable=labelNULL2, font="Verdana 14 normal")
output_labelNULL2.grid(row=1, column=4)

output_labelNULL2 = tk.Label(output_frame, textvariable=labelNULL2, font="Verdana 14 normal")
output_labelNULL2.grid(row=2, column=4)

output_labelNULL3 = tk.Label(output_frame, textvariable=labelNULL3, font="Verdana 14 normal")
output_labelNULL3.grid(row=0, column=6)

output_labelNULL3 = tk.Label(output_frame, textvariable=labelNULL3, font="Verdana 14 normal")
output_labelNULL3.grid(row=1, column=6)

output_labelNULL3 = tk.Label(output_frame, textvariable=labelNULL3, font="Verdana 14 normal")
output_labelNULL3.grid(row=2, column=6)

#Новая вставка с постоянным текстом
#Делаем так, чтобы надписи были всегда
# output_text1.set('Выходное напряжение [В]: ')
# output_text2.set('Load regulation [%]: ')
# output_text3.set('Line regulation [%]: ')
# output_text4.set('КПД [%]: ')
# output_text5.set('Пульсации  [мВ p-p]: ')
# output_text6.set('Напряжение отключения [В]: ')


# Start GUI event loop
root.mainloop()