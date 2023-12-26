import tkinter as tk

def highlight_text(event):
    event.widget.tag_remove("highlight", "1.0", "end")
    event.widget.tag_add("highlight", "1.0", "end")

def clear_highlight(event):
    event.widget.tag_remove("highlight", "1.0", "end")

def get_input():
    input_text = input_entry.get("1.0", "end-1c")
    output_text = f"Input: {input_text}"
    output_label.config(text=output_text)

root = tk.Tk()
root.title("Highlighted Input and Output")

# Create a LabelFrame for input
input_frame = tk.LabelFrame(root, text="Input")
input_frame.pack(padx=10, pady=10)

# Create an input text widget
input_entry = tk.Text(input_frame, height=5, width=30)
input_entry.pack()

# Bind events to highlight the input area
input_entry.bind("<FocusIn>", highlight_text)
input_entry.bind("<FocusOut>", clear_highlight)

# Create a LabelFrame for output
output_frame = tk.LabelFrame(root, text="Output")
output_frame.pack(padx=10, pady=10)

# Create an output label
output_label = tk.Label(output_frame, text="Output: ")
output_label.pack()

# Create a button to get input and display output
get_input_button = tk.Button(root, text="Get Input", command=get_input)
get_input_button.pack(pady=10)

# Configure tags for highlighting
input_entry.tag_configure("highlight", background="yellow")

root.mainloop()