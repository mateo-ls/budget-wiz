from tkinter import *

# --- functions ---

def create_frame(master):
    print("create frame")

    frame = Frame(master)

    b = Button(frame, text='Do Something')
    b.pack(pady=10)

    clearall = Button(frame, text='reset', command=reset_all)
    clearall.pack(pady=10)

    return frame

def reset_all():
    global frame

    frame.destroy()
    frame = create_frame(master)
    #frame = create_different_frame(master)
    frame.pack()

# --- main ---


master = Tk()

frame = create_frame(master)
frame.pack()

mainloop()