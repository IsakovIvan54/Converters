import tkinter as tk
import pygame

pygame.mixer.init()


def run_script():
    # Your script code goes here
    # input_data = InPutV1.get() + InPutV2.get() + InPutV3.get()
    # output_text.set('Script output: ' + input_data)
    print(InPutV1.get(), InPutV2.get())
    output_text1.set('Выходное напряжение [В]: ' + InPutV1.get())
    output_text2.set('Load regulation [%]: ' + InPutV1.get())
    output_text3.set('Line regulation [%]: ' + InPutV1.get())
    output_text4.set('КПД [%]: ' + InPutV1.get()),
    output_text5.set('Пульсации  [мВ p-p]: ' + InPutV1.get())
    # Пример того как можно переводить входные данные в целые числа
    VoutLoadNom = float(InPutV1.get())
    LineReg = float(InPutV1.get())
    LoadReg = float(InPutV1.get())
    RipleRMS = float(InPutV1.get())
    # b = int(InPutV2.get())
    # print(a+b)
    accur_output_voltage = float(АcOutVolt.get())
    nominal_output_voltage = float(NomOutVolt.get())
    
    max_line_reg = float(MaxLineReg.get())
    max_load_reg = float(MaxLoadReg.get())
    # nominal_kpd = float(NominalKpd.get())
    max_riple_abs = float(MaxRipple.get())
    max_riple_per = float(MaxRipple.get())
    print((nominal_output_voltage - nominal_output_voltage*accur_output_voltage/100))

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

    pygame.mixer.music.load('sound.wav')
    pygame.mixer.music.play(0)

def exit_window():
    root.destroy()

root = tk.Tk()

root.geometry('760x220')

# Create GUI widgets
# Данные с первой строки
tk.Label(root, text='Минимальное входное напряжение[В]:').grid(row=0, column=0)
InPutV1 = tk.Entry(root)
InPutV1.grid(row=0, column=1)

tk.Label(root, text='Номинальное входное напряжение[В]:').grid(row=1, column=0)
InPutV2 = tk.Entry(root)
InPutV2.grid(row=1, column=1)

tk.Label(root, text='Максимальное входное напряжение[В]:').grid(row=2, column=0)
InPutV3 = tk.Entry(root)
InPutV3.grid(row=2, column=1)

tk.Label(root, text='Ток нагрузки[А]:').grid(row=3, column=0)
OutCurr = tk.Entry(root)
OutCurr.grid(row=3, column=1)

tk.Label(root, text='Номинальное выходное напряжение[V]:').grid(row=4, column=0)
NomOutVolt = tk.Entry(root)
NomOutVolt.grid(row=4, column=1)


tk.Label(root, text='Отклонение выходного напряжения[%]:').grid(row=0, column=2)
АcOutVolt = tk.Entry(root)
АcOutVolt.grid(row=0, column=3)

tk.Label(root, text='Line regulation max[%]:').grid(row=1, column=2)
MaxLineReg = tk.Entry(root)
MaxLineReg.grid(row=1, column=3)

tk.Label(root, text='Load regulation max[%]:').grid(row=2, column=2)
MaxLoadReg = tk.Entry(root)
MaxLoadReg.grid(row=2, column=3)

tk.Label(root, text='Номинальный КПД[%]:').grid(row=3, column=2)
NominalKpd = tk.Entry(root)
NominalKpd.grid(row=3, column=3)

# textRip='Максимумальные пульсации[%]:'

def toggle_flag():
    if flag_var.get() == 1:
        tk.Label(root, text= 'Максимальные пульсации[%]:').grid(row=4, column=2)
        MaxRipple = tk.Entry(root)
        MaxRipple.grid(row=4, column=3)
    else:
        tk.Label(root, text= 'Максимальные пульсации[mV]:').grid(row=4, column=2)
        MaxRipple = tk.Entry(root)
        MaxRipple.grid(row=4, column=3)

tk.Label(root, text='Максимальные пульсации[mV]:').grid(row=4, column=2)
MaxRipple = tk.Entry(root)
MaxRipple.grid(row=4, column=3)

flag_var = tk.IntVar()

checkbox = tk.Checkbutton(root, text="Flag", variable=flag_var, command=toggle_flag)
checkbox.grid(row=4, column=4)


run_button = tk.Button(root, text='Run', command=run_script)
run_button.grid(row=6, column=2)

exit_button = tk.Button(root, text='Exit', command=exit_window)
exit_button.grid(row=6, column=3)



output_text1 = tk.StringVar()
output_label1 = tk.Label(root, textvariable=output_text1)
output_label1.grid(row=5, columnspan=2)

output_text2 = tk.StringVar()
output_label2 = tk.Label(root, textvariable=output_text2)
output_label2.grid(row=6, columnspan=2)

output_text3 = tk.StringVar()
output_label3 = tk.Label(root, textvariable=output_text3)
output_label3.grid(row=7, columnspan=2)

output_text4 = tk.StringVar()
output_label4 = tk.Label(root, textvariable=output_text4)
output_label4.grid(row=8, columnspan=2)

output_text5 = tk.StringVar()
output_label5 = tk.Label(root, textvariable=output_text5)
output_label5.grid(row=9, columnspan=2)

#Делаем так, чтобы надписи были всегда
output_text1.set('Выходное напряжение [В]: ')
output_text2.set('Load regulation [%]: ')
output_text3.set('Line regulation [%]: ')
output_text4.set('КПД [%]: '),
output_text5.set('Пульсации  [мВ p-p]: ')

# Start GUI event loop
root.mainloop()