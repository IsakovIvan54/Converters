import tkinter as tk
import pygame
from PIL import Image, ImageTk

# Define the range of data
min_data = 0
max_data = 100

# Initialize Pygame mixer for sound playback
pygame.mixer.init()

# Function to compare the input data with the range and update the label and color accordingly
def compare_data():
    input_data = int(entry.get())
    
    if min_data <= input_data <= max_data:
        label.config(text="Data is within the range", fg="green")
    else:
        label.config(text="Data is not within the range", fg="red")
    
    # Play a sound
    pygame.mixer.music.load('sound.wav')
    pygame.mixer.music.play(0)

# Create the main window
window = tk.Tk()
window.title("Data Range Checker")

# Create an entry field for input data
entry = tk.Entry(window)
entry.grid(row=1, column=0)


# Create a button to perform the comparison
button = tk.Button(window, text="Compare", command=compare_data)
button.grid(row=2, column=0)


# Create a label to display the result
label = tk.Label(window, text="")
label.grid(row=2, column=1)

label2 = tk.Label(window, text="123NOW")
label2.grid(row=2, column=2)

# Load and display an image
image = Image.open("image.jpg")
image = image.resize((200, 200), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=photo)
image_label.grid(row=4, column=0)

# Start the Tkinter event loop
window.mainloop()