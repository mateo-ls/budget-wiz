# Import the required libraries
from tkinter import *

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Define a function update the label text
def on_click():
   label["text"] = "Python"
   b["state"] = "disabled"

# Create a label widget
label = Label(win, text="Click the Button to update this Text",
font=('Calibri 15 bold'))
label.pack(pady=20)

# Create a button to update the label widget
b = Button(win, text="Update Label", command=on_click)
b.pack(pady=20)



win.mainloop()