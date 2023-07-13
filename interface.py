import tkinter as tk

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
    a = int(InPutV1.get())
    b = int(InPutV2.get())
    print(a+b)
    

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