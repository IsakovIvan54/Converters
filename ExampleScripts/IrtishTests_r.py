import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np
from PIL import Image, ImageTk


dateString_reg_down = 'Reg_down'
dateString_reg_up = 'Reg_up'

filepath_reg_down = "./" + dateString_reg_down + ".csv"
filepath_reg_up = "./" + dateString_reg_up + ".csv"

rm = pyvisa.ResourceManager()

pygame.mixer.init()
print(rm.list_resources())

rm = pyvisa.ResourceManager()
RIG_DL3031A = rm.open_resource('USB0::0x1AB1::0x0E11::DL3D244200321::INSTR')
AKIP = rm.open_resource('TCPIP0::192.168.0.175::HISLIP0::INSTR')
KEITHDMM6500 = rm.open_resource('USB0::0x05E6::0x6500::04530036::INSTR')
RIG_DL831A = rm.open_resource('USB0::0x1AB1::0x0E11::DP8A244400389::INSTR')
RIG_MSO8104 = rm.open_resource('USB0::0x1AB1::0x0516::DS8A242800498')

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


# Настройка осциллографа
RIG_MSO8104.write(':CHAN1:DISP ON')  # enable channel 1 display
RIG_MSO8104.write(':CHAN1:COUP AC ')  # DC coupling
RIG_MSO8104.write(':CHAN1:IMP OMEG')  # 1 MOhm input impedance
RIG_MSO8104.write(':CHAN1:PROBE 1')  # 1x probe attenuation
RIG_MSO8104.write(':CHAN1:BWL 20M')
RIG_MSO8104.write(':CHAN1:SCAL 0.1')
RIG_MSO8104.write(':TIM:SCAL 0.000002')


def run_TEST(INVOLT, OUTCURR, DVolt):
    time.sleep(1)
    AKIP.write('SOUR:VOLT ' + str(INVOLT))
    RIG_DL3031A.write('CURR ' + str(OUTCURR))
    RIG_DL831A.write(f':SOUR1:VOLT {DVolt}')

    AKIP.write(':OUTP ON')
    RIG_DL831A.write('OUTP CH1, ON')

    time.sleep(1)

    currentHH = float(AKIP.query('MEAS:CURR?')) # Входный ток без нагрузки
    voltageHH = float(AKIP.query('MEAS:VOLT?')) # Входное напряжение без нагрузки

    time.sleep(2)

    voltageHHout = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?')) # Выходное напряжение без нагрузки

    time.sleep(0.2)

    RIG_DL3031A.write(':INP ON')

    time.sleep(2)


    currentLOAD = float(AKIP.query('MEAS:CURR?')) # Входный ток c нагрузкой
    voltageLOAD = float(AKIP.query('MEAS:VOLT?')) # Входное напряжение c нагрузкой

    voltageLOADout = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?')) # Выходное напряжение  c нагрузкой
    currentLOADout = float(RIG_DL3031A.query('MEAS:CURR?')) # Выходной ток c нагрузкой

    RIG_MSO8104.write(':MEAS:STAT:ITEM VRMS,CHAN1')


    Noise = float(RIG_MSO8104.query(':MEAS:ITEM? VRMS,CHAN1')) * 1000
    NoisePP = float(RIG_MSO8104.query(':MEAS:ITEM? VPP,CHAN1')) * 1000


    kpd = ((voltageLOADout * currentLOADout) / (currentLOAD * voltageLOAD)) * 100

    RIG_DL3031A.write(':INP OFF')
    AKIP.write(':OUTP OFF')
    RIG_DL831A.write('OUTP CH1, OFF')

    
    
    print('------------------------------------------------------------------------')

    print(f'Напряжение ХХ: {voltageHHout:.3f}')
    print(f'Входной ток ХХ: {currentHH:.3f} A, Входное напряжение ХХ: {voltageHH:.3f} V')
    

    print(f'Напряжение под нагрузкой: {voltageLOADout:.3f} V, Ток под нагрузкой: {currentLOADout:.3f} A')
    print(f'Входной ток под нагрузкой: {currentLOAD:.3f} A, Входное напряжение под нагрузкой: {voltageLOAD:.3f} V')
    print(f'КПД: {kpd:.1f} %')
    print(f'Пульсации Vrms: {Noise:.1f} mV')
    print(f'Пульсации Vp-p: {NoisePP:.1f} mV')
    return[voltageHHout, voltageLOADout, kpd, Noise, NoisePP]

def show_devices():
    try:
        # Initialize the pyvisa library
        rm = pyvisa.ResourceManager()

        # Get a list of all connected devices
        devices = rm.list_resources()

        # Display a pop-up list with the name and VISA resource of each device
        messagebox.showinfo("Connected Devices", "\n".join(devices))

        # Close the resource manager
        rm.close()
    except pyvisa.Error as e:
        messagebox.showerror("Error", f"Error accessing devices: {e}")

def Disable_Volt(INVOLT, OUTCURR, DVolt, nominal_output_voltage):
    time.sleep(1)
    AKIP.write('SOUR:VOLT ' + str(INVOLT))
    RIG_DL3031A.write('CURR ' + str(OUTCURR))

    AKIP.write(':OUTP ON')
    time.sleep(1)

    RIG_DL3031A.write(':INP ON')
    RIG_DL831A.write('OUTP CH1, ON')
    RIG_DL831A.write(f':SOUR1:VOLT {DVolt}')
    time.sleep(1)

    for VoltageDis in np.arange(DVolt,0,-0.05):
        
        RIG_DL831A.write(f':SOUR1:VOLT {VoltageDis}')
        time.sleep(0.1)
        voltageOUT = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))
        
        if voltageOUT <= nominal_output_voltage/2:
            break
    RIG_DL831A.write('OUTP CH1, OFF')
    RIG_DL3031A.write(':INP OFF')
    AKIP.write(':OUTP OFF')
    print("Напряжение отключения [V]" + str(VoltageDis))

    return VoltageDis

def Disable_Volt_NOLOAD(INVOLT, DVolt, nominal_output_voltage):
    time.sleep(1)
    AKIP.write('SOUR:VOLT ' + str(INVOLT))
    

    AKIP.write(':OUTP ON')
    time.sleep(1)

    RIG_DL831A.write(f':SOUR1:VOLT {DVolt}')
    RIG_DL831A.write('OUTP CH1, ON')
    time.sleep(1)

    for VoltageDis in np.arange(DVolt,0,-0.05):
        RIG_DL831A.write(f':SOUR1:VOLT {VoltageDis}')
        time.sleep(0.1)
        voltageOUT = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))
        print(voltageOUT)
        if voltageOUT <= nominal_output_voltage*0.99:
            break
    RIG_DL831A.write('OUTP CH1, OFF')
    AKIP.write(':OUTP OFF')

    return VoltageDis

def reg_Down(INVOLT, OUTCURR, DVolt, nominal_output_voltage): # Крутить с крайнего левого положения в правое

    dateString_reg_down =  NameConverter.get() + 'Reg_down'
    filepath_reg_down = "./" + dateString_reg_down + ".csv"
    
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

    with open(filepath_reg_down, "a") as file:
        if os.stat(filepath_reg_down).st_size == 0: #if empty file, write a nice header
            file.write("Регулировка" + str(intervals[0]) + " От номинального [V];" + "Регулировка" + str(intervals[1]) + " От номинального [V];" + "Регулировка" + str(intervals[2]) + " От номинального [V];" + "Регулировка" + str(intervals[3]) + " От номинального [V]; "+"Регулировка" + str(intervals[4]) + " От номинального [V];"+ "Регулировка" + str(intervals[5]) + " От номинального [V];" + "Регулировка" + str(intervals[6]) + " От номинального [V];" +"\n")
        file.write("{};{};{};{};{};{};{};\n".format(value[0], value[1], value[2], value[3], value[4], value[5], value[6])) # log the data
    file.close()
    return value
    
def reg_Up(INVOLT, OUTCURR, DVolt, nominal_output_voltage): # Крутить с крайнего правого положения в левое
   
    dateString_reg_up = NameConverter.get() + 'Reg_up'
    filepath_reg_up = "./" + dateString_reg_up + ".csv"

    intervals = [1.05, 1.1]
    value = [0, 0]

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


    while VoltOut <= intervals[1]*nominal_output_voltage  :
        VoltOut = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?'))
        print ('Напряжение регулировки: ' + str(VoltOut))
        if VoltOut <= 1.05*nominal_output_voltage:
            value[0] = VoltOut
        elif (VoltOut > 1.05*nominal_output_voltage) & (VoltOut <= 1.1*nominal_output_voltage):
            value[1] = VoltOut

        
    print(value)

    RIG_DL831A.write('OUTP CH1, OFF')
    AKIP.write(':OUTP OFF')
    RIG_DL3031A.write(':INP OFF')

    with open(filepath_reg_up, "a") as file:
        if os.stat(filepath_reg_up).st_size == 0: #if empty file, write a nice header
            file.write("Регулировка" + str(intervals[0]) + " От номинального [V];" + "Регулировка" + str(intervals[1]) +"\n")
        file.write("{};{};\n".format(value[0], value[1])) # log the data
    file.close()
    return value

def run_script():

    dateString = NameConverter.get()
    filepath = "./" + dateString + ".csv"
    

    

    


    VolInMin = int(InPutV1.get())
    VolInNom = int(InPutV2.get())
    VolInMax = int(InPutV3.get())
    IoutNom = float(OutCurr.get())

    accur_output_voltage = float(АcOutVolt.get())
    nominal_output_voltage = float(NomOutVolt.get())
    max_line_reg = float(MaxLineReg.get())
    max_load_reg = float(MaxLoadReg.get())
    # nominal_kpd = float(NominalKpd.get())
    max_riple_abs = float(MaxRipple.get())
    max_riple_per = float(MaxRipple.get())
    disable_volt = float(DisVolt.get())
    disable_volt_max = float(DisVoltMax.get())
    disable_volt_min = float(DisVoltMin.get())
    

    valueMin = run_TEST(VolInMin, IoutNom, disable_volt)
    valueNom = run_TEST(VolInNom, IoutNom, disable_volt)
    valueMax = run_TEST(VolInMax, IoutNom, disable_volt)

    DisableVoltage = round(Disable_Volt(VolInNom, IoutNom, disable_volt, nominal_output_voltage),3)
    # DisableVoltageMax = Disable_Volt(VolInNom, disable_volt, nominal_output_voltage)

    VoutNoLoadNOM = round(valueNom[0], 3)
    VoutLoadMin = round(valueMin[1], 3)
    VoutLoadNom = round(valueNom[1], 3)
    VoutLoadMax = round(valueMax[1], 3)

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
    if (flag_var.get() == 0):
        if ((RipleRMS <= max_riple_abs)):
            output_label5.config(fg="green")
        else: 
            output_label5.config(fg="red")
    else:
        if ((RipleRMS <= nominal_output_voltage*max_riple_per/100)):
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
            file.write("Выходное напряжение (без нагрузки) [V]; Выходное напряжение при Vin" + str(VolInMin) + " [V];" + "Выходное напряжение при Vin" + str(VolInNom)+ " [V];" + "Выходное напряжение при Vin" + str(VolInMax)+ " [V];" + "LineReg [%]; LoadReg [%]; Пульсации [мВp-p];ПульсацииRMS [мВ];" + "КПД при Vin" + str(VolInMin) + " [V];" + "КПД при Vin" + str(VolInNom)+ " [V];" + "КПД при Vin" + str(VolInMax)+ " [V];" + "Напряжение отключения [V];" +"\n")
        file.write("{};{};{};{};{};{};{};{};{};{};{};{}\n".format(VoutNoLoadNOM, VoutLoadMin, VoutLoadNom, VoutLoadMax, LineReg, LoadReg,RiplePP, RipleRMS, KPDMin, KPDNom, KPDMax, DisableVoltage)) # log the data
    file.close()

    pygame.mixer.music.load('sound.wav')
    pygame.mixer.music.play(0)

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

root = tk.Tk()
root.title('Программное обеспечение для проверки DC-DC преобразователей серии "Иртыш"')
# Create GUI widgets
# Данные с первой строки
root.geometry("1550x600")

tk.Label(root, text='Проверка DC-DC преобразователей серии "Иртыш"', font="Verdana 14 normal").place(x=500, y=0)

tk.Label(root, text='Наименование преобразователя:', font="Verdana 14 normal").place(x=500, y=35)
NameConverter = tk.Entry(root,font=("Arial", 14))
NameConverter.place(x=830, y=35)

tk.Label(root, text='Версия:1.0.1', font="Verdana 8 normal").place(x=0, y=580)

label_image1 = Image.open("EKBlogoNew.png")
img=label_image1.resize((95, 70))
label_image = ImageTk.PhotoImage(img)
tk.Label(root, image=label_image).place(x=1445, y=520)

# Create a LabelFrame for output
input_frame = tk.LabelFrame(root, text="Параметры преобразователя", font=("Arial", 14))
input_frame.pack(padx=10, pady=10, ipadx=10, ipady=10)
input_frame.place(x=0, y=70)


button_frame = tk.LabelFrame(root, text="Меню", font=("Arial", 14))
button_frame.pack(padx=10, pady=10)
button_frame.place(x=250, y=380)


output_frame = tk.LabelFrame(root, text="Измеренные параметры преобразователя", font=("Arial", 14))
output_frame.pack(padx=10, pady=10)
output_frame.place(x=750, y=380)


tk.Label(input_frame, text='Минимальное входное напряжение[В]:', font="Verdana 14 normal").grid(row=0, column=0)
InPutV1 = tk.Entry(input_frame,font=("Arial", 14))
InPutV1.grid(row=0, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальное входное напряжение[В]:', font="Verdana 14 normal").grid(row=1, column=0)
InPutV2 = tk.Entry(input_frame,font=("Arial", 14))
InPutV2.grid(row=1, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Максимальное входное напряжение[В]:', font="Verdana 14 normal").grid(row=2, column=0)
InPutV3 = tk.Entry(input_frame,font=("Arial", 14))
InPutV3.grid(row=2, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Ток нагрузки[А]:', font="Verdana 14 normal").grid(row=3, column=0)
OutCurr = tk.Entry(input_frame,font=("Arial", 14))
OutCurr.grid(row=3, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальное выходное напряжение[V]:', font="Verdana 14 normal").grid(row=4, column=0)
NomOutVolt = tk.Entry(input_frame,font=("Arial", 14))
NomOutVolt.grid(row=4, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Начальное напряжение на управляющем входе[В]:', font="Verdana 14 normal").grid(row=5, column=0)
DisVolt = tk.Entry(input_frame,font=("Arial", 14))
DisVolt.grid(row=5, column=1,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Отклонение выходного напряжения[%]:', font="Verdana 14 normal").grid(row=0, column=2)
АcOutVolt = tk.Entry(input_frame,font=("Arial", 14))
АcOutVolt.grid(row=0, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Line regulation max[%]:', font="Verdana 14 normal").grid(row=1, column=2)
MaxLineReg = tk.Entry(input_frame,font=("Arial", 14))
MaxLineReg.grid(row=1, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Line regulation max[%]:', font="Verdana 14 normal").grid(row=2, column=2)
MaxLoadReg = tk.Entry(input_frame,font=("Arial", 14))
MaxLoadReg.grid(row=2, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Номинальный КПД[%]:', font="Verdana 14 normal").grid(row=3, column=2)
NominalKpd = tk.Entry(input_frame,font=("Arial", 14))
NominalKpd.grid(row=3, column=3,  ipadx=6, ipady=7)

def toggle_flag():
    if flag_var.get() == 1:
        tk.Label(input_frame, text= 'Максимальные пульсации[%]:', font="Verdana 14 normal").grid(row=4, column=2)
        MaxRippleP = tk.Entry(input_frame,font=("Arial", 14))
        MaxRippleP.grid(row=4, column=3,  ipadx=6, ipady=7)
    else:
        tk.Label(input_frame, text= 'Максимальные пульсации[mV]:', font="Verdana 14 normal").grid(row=4, column=2)
        MaxRippleV = tk.Entry(input_frame,font=("Arial", 14))
        MaxRippleV.grid(row=4, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text= 'Максимальные пульсации[mV]:', font="Verdana 14 normal").grid(row=4, column=2)
MaxRipple = tk.Entry(input_frame,font=("Arial", 14))
MaxRipple.grid(row=4, column=3,  ipadx=6, ipady=7)


tk.Label(input_frame, text='Минимальное управляющее напряжение[В]:', font="Verdana 14 normal").grid(row=5, column=2)
DisVoltMin = tk.Entry(input_frame,font=("Arial", 14))
DisVoltMin.grid(row=5, column=3,  ipadx=6, ipady=7)

tk.Label(input_frame, text='Максимальное управляющее напряжение[В]:', font="Verdana 14 normal").grid(row=6, column=2)
DisVoltMax = tk.Entry(input_frame,font=("Arial", 14))
DisVoltMax.grid(row=6, column=3,  ipadx=6, ipady=7)

flag_var = tk.IntVar()

checkbox = tk.Checkbutton(input_frame, text="[mV/%]", variable=flag_var, command=toggle_flag)
checkbox.grid(row=4, column=4)


run_button = tk.Button(button_frame, text='Запуск проверки', command=run_script)
run_button.config(width=20, height=2)
run_button.grid(row=0, column=1)

reg_down_button = tk.Button(button_frame, text='Регулировка вверх', command=reg_Down_But)
reg_down_button.config(width=20, height=2)
reg_down_button.grid(row=1, column=0)

reg_down_button = tk.Button(button_frame, text='Регулировка вниз', command=reg_Up_But)
reg_down_button.config(width=20, height=2)
reg_down_button.grid(row=0, column=0)

exit_button = tk.Button(button_frame, text='Выход', command=exit_window)
exit_button.config(width=20, height=2)
exit_button.grid(row=1, column=1)

output_text1 = tk.StringVar()
output_label1 = tk.Label(output_frame, textvariable=output_text1, font="Verdana 14 normal")
output_label1.grid(row=6, columnspan=2)

output_text2 = tk.StringVar()
output_label2 = tk.Label(output_frame, textvariable=output_text2, font="Verdana 14 normal")
output_label2.grid(row=7, columnspan=2)

output_text3 = tk.StringVar()
output_label3 = tk.Label(output_frame, textvariable=output_text3, font="Verdana 14 normal")
output_label3.grid(row=8, columnspan=2)

output_text4 = tk.StringVar()
output_label4 = tk.Label(output_frame, textvariable=output_text4, font="Verdana 14 normal")
output_label4.grid(row=6, column=3)

output_text5 = tk.StringVar()
output_label5 = tk.Label(output_frame, textvariable=output_text5, font="Verdana 14 normal")
output_label5.grid(row=7, column=3)

output_text6 = tk.StringVar()
output_label6 = tk.Label(output_frame, textvariable=output_text6, font="Verdana 14 normal")
output_label6.grid(row=8, column=3)

#Новая вставка с постоянным текстом
#Делаем так, чтобы надписи были всегда
output_text1.set('Выходное напряжение [В]: ')
output_text2.set('Load regulation [%]: ')
output_text3.set('Line regulation [%]: ')
output_text4.set('КПД [%]: '),
output_text5.set('Пульсации  [мВ p-p]: ')
output_text6.set('Напряжение отключения [В]: ')

# Start GUI event loop
root.mainloop()