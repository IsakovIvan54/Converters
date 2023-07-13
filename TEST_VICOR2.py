import pyvisa
import time
import os
import tkinter as tk
from tkinter import messagebox
dateString = 'ET-Q300H-15VP150R23'
# dateString = time.strftime("%Y-%m-%d_%H%M")
filepath = "./" + dateString + ".csv"

rm = pyvisa.ResourceManager()

print(rm.list_resources())

rm = pyvisa.ResourceManager()
RIG_DL3031A = rm.open_resource('USB0::0x1AB1::0x0E11::DL3D244200321::INSTR')
AKIP = rm.open_resource('TCPIP0::192.168.0.175::HISLIP0::INSTR')
KEITHDMM6500 = rm.open_resource('USB0::0x05E6::0x6500::04530036::INSTR')
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


# Настройка осциллографа

RIG_MSO8104.write(':CHAN1:DISP ON')  # enable channel 1 display
RIG_MSO8104.write(':CHAN1:COUP AC ')  # DC coupling
RIG_MSO8104.write(':CHAN1:IMP OMEG')  # 1 MOhm input impedance
RIG_MSO8104.write(':CHAN1:PROBE 1')  # 1x probe attenuation
RIG_MSO8104.write(':CHAN1:BWL 20M')
RIG_MSO8104.write(':CHAN1:SCAL 0.1')
RIG_MSO8104.write(':TIM:SCAL 0.000002')





def run_TEST(INVOLT, OUTCURR):
    time.sleep(1)
    AKIP.write('SOUR:VOLT ' + str(INVOLT))
    RIG_DL3031A.write('CURR ' + str(OUTCURR))

    AKIP.write(':OUTP ON')

    time.sleep(1)

    currentHH = float(AKIP.query('MEAS:CURR?')) # Входный ток без нагрузки
    voltageHH = float(AKIP.query('MEAS:VOLT?')) # Входное напряжение без нагрузки

    voltageHHout = float(KEITHDMM6500.query(':MEASURE:VOLTAGE:DC?')) # Выходное напряжение без нагрузки

    time.sleep(2)

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

    


    print(f'Напряжение ХХ: {voltageHHout:.3f}')
    print(f'Входной ток ХХ: {currentHH:.3f} A, Входное напряжение ХХ: {voltageHH:.3f} V')
    print('------------------------------------------------------------------------')

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

def run_script():




    VolInMin = int(InPutV1.get())
    VolInNom = int(InPutV2.get())
    VolInMax = int(InPutV3.get())
    IoutNom = float(OutCurr.get())

    valueMin = run_TEST(VolInMin, IoutNom)
    valueNom = run_TEST(VolInNom, IoutNom)
    valueMax = run_TEST(VolInMax, IoutNom)

    VoutNoLoadNOM = valueNom[0]
    VoutLoadMin = valueMin[1]
    VoutLoadNom = valueNom[1]
    VoutLoadMax = valueMax[1]

    LineReg = max(((VoutLoadNom - VoutLoadMin) / VoutLoadNom * 100), ((VoutLoadNom - VoutLoadMax) / VoutLoadNom * 100))
    LoadReg = (VoutLoadNom - VoutNoLoadNOM) / VoutLoadNom * 100

    RiplePP = valueNom[4]
    RipleRMS = valueNom[3]

    KPDMin = valueMin[2]
    KPDNom = valueNom[2]
    KPDMax = valueMax[2]

    output_text1.set('Выходное напряжение [В]: ' + str(VoutLoadNom))
    output_text2.set('Load regulation [%]: ' + str(LoadReg))
    output_text3.set('Line regulation [%]: ' + str(LineReg))
    output_text4.set('КПД [%]: ' + str(KPDNom)),
    output_text5.set('Пульсации  [мВ p-p]: ' + str(RiplePP))

    # Write results to a file
    with open(filepath, "a") as file:
        if os.stat(filepath).st_size == 0: #if empty file, write a nice header
            file.write("Выходное напряжение (без нагрузки) [V]; Выходное напряжение при Vin" + str(VolInMin) + " [V];" + "Выходное напряжение при Vin" + str(VolInNom)+ " [V];" + "Выходное напряжение при Vin" + str(VolInMax)+ " [V];" + "LineReg [%]; LoadReg [%]; Пульсации [мВp-p];ПульсацииRMS [мВ];" + "КПД при Vin" + str(VolInMin) + " [V];" + "КПД при Vin" + str(VolInNom)+ " [V];" + "КПД при Vin" + str(VolInMax)+ " [V];" +"\n")
        file.write("{};{};{};{};{};{};{};{};{};{};{}\n".format(VoutNoLoadNOM, VoutLoadMin, VoutLoadNom, VoutLoadMax, LineReg, LoadReg,RiplePP, RipleRMS, KPDMin, KPDNom, KPDMax)) # log the data
    file.close()

    
    

def exit_window():
    root.destroy()

root = tk.Tk()

# Create GUI widgets
# Данные с первой строки
tk.Label(root, text='Введите минимальное входное напряжение[В]:').grid(row=0, column=0)
InPutV1 = tk.Entry(root)
InPutV1.grid(row=0, column=1)

tk.Label(root, text='Введите номинальное входное напряжение[В]:').grid(row=1, column=0)
InPutV2 = tk.Entry(root)
InPutV2.grid(row=1, column=1)

tk.Label(root, text='Введите максимальное входное напряжение[В]:').grid(row=2, column=0)
InPutV3 = tk.Entry(root)
InPutV3.grid(row=2, column=1)

tk.Label(root, text='Введите ток нагрузки[А]:').grid(row=3, column=0)
OutCurr = tk.Entry(root)
OutCurr.grid(row=3, column=1)


run_button = tk.Button(root, text='Run', command=run_script)
run_button.grid(row=4, column=0)

exit_button = tk.Button(root, text='Exit', command=exit_window)
exit_button.grid(row=4, column=1)

# show_devices_button = tk.Button(root, text="Show Devices", command=show_devices)
# show_devices_button.grid(row=4, column=2)

output_text1 = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text1)
output_label.grid(row=5, columnspan=1)

output_text2 = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text2)
output_label.grid(row=6, columnspan=1)

output_text3 = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text3)
output_label.grid(row=7, columnspan=1)

output_text4 = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text4)
output_label.grid(row=8, columnspan=1)

output_text5 = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text5)
output_label.grid(row=9, columnspan=1)

# Start GUI event loop
root.mainloop()







