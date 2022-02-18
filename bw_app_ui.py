import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
import mysql.connector


class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # This container is where we'll stack all the frames for different pages
        # on top of each other, and the one we want to be visible will be
        # raised on top of all the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TransactionPage, AddTransactionPage, EditTransactionPage, AnalyticsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # All frames are stacked on top of each other
            # The one on top will be the one visible
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TransactionPage")
    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class TransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        # Establishes this pages UI elements/widgets

        # Buttons
        selfButton = tk.Button(self, text="Transactions")
        analyticsButton = tk.Button(self, text="Analytics")
        addButton = tk.Button(self, text="Add", command=lambda: controller.show_frame("AddTransactionPage"))
        editButton = tk.Button(self, text="Edit")
        deleteButton = tk.Button(self, text="Delete")
        thisMonthButton = tk.Button(self, text="This Month")
        
        # Image Buttons (Left and Right Arrows)
        # Getting this to work was really dumb
        # Let's stay away from image UI elements
        arrowImage = Image.open('resources\\arrow_icon.png')
        arrowImage = arrowImage.resize((30, 30), Image.ANTIALIAS)
        arrowImageFlipped = Image.open('resources\\arrow_icon_flipped.png')
        arrowImageFlipped = arrowImageFlipped.resize((30, 30), Image.ANTIALIAS)
        arrowIcon = ImageTk.PhotoImage(arrowImage)
        arrowIconFlipped = ImageTk.PhotoImage(arrowImageFlipped)
        leftArrowButton = tk.Button(self, image=arrowIcon, borderwidth=0)
        leftArrowButton.image = arrowIcon
        rightArrowButton = tk.Button(self, image=arrowIconFlipped, borderwidth=0)
        rightArrowButton.image = arrowIconFlipped

        # Labels (text)
        selectedMonthLabel = tk.Label(self, text="February 2022")
        incomeLabel = tk.Label(self, text="Incomes")
        expenseLabel = tk.Label(self, text="Expenses")
        label = tk.Label(self, text="This is Transaction Page")


        # Establishes layout of above elements
        # Buttons
        selfButton.grid(row=0, column=0)
        analyticsButton.grid(row=0, column=1)
        deleteButton.grid(row=0, column=7)
        editButton.grid(row=0, column=6)
        addButton.grid(row=0, column=5)
        thisMonthButton.grid(row=1, column=4)

        # Image Buttons
        leftArrowButton.grid(row=1, column=1)
        rightArrowButton.grid(row=1, column=3)

        #Labels
        selectedMonthLabel.grid(row=1, column=2)
        incomeLabel.grid(row=2, column=2)
        expenseLabel.grid(row=2, column=5)
        label.grid(row=5, column=5)


        # Sets minimun sizes for all columns or rows
        # Might want to change/get rid of this later
        columnCount, rowCount = self.grid_size()
        for column in range(columnCount):
            self.grid_columnconfigure(column, minsize=100)
        for row in range(rowCount):
            self.grid_rowconfigure(row, minsize=100)
       

class AddTransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        transactionsButton = tk.Button(self, text="Back to Transactions", command=lambda: controller.show_frame("TransactionPage"))
        transactionsButton.grid(row=0, column=0)

        label = tk.Label(self, text="This is Add Transaction Page")
        label.grid(row=1, column=0)

class EditTransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Edit Transaction Page")
        label.pack(side="top", fill="both", expand=True)

class AnalyticsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Analytics Page")
        label.pack(side="top", fill="both", expand=True)

        arrowImage = Image.open('resources\\arrow_icon.png')
        arrowImage = arrowImage.resize((30, 30), Image.ANTIALIAS)
        arrowImageFlipped = Image.open('resources\\arrow_icon_flipped.png')
        arrowImageFlipped = arrowImageFlipped.resize((30, 30), Image.ANTIALIAS)
        arrowIcon = ImageTk.PhotoImage(arrowImage)
        arrowIconFlipped = ImageTk.PhotoImage(arrowImageFlipped)
        leftArrowButton = tk.Button(self, image=arrowIcon, borderwidth=0)
        leftArrowButton.image = arrowIcon
        rightArrowButton = tk.Button(self, image=arrowIconFlipped, borderwidth=0)
        rightArrowButton.image = arrowIconFlipped
        

if __name__ == "__main__":
    # At some point we can set our own custom icon
    # root.iconbitmap(default='')
    
    main = MainView()
    main.wm_geometry("800x800")
    main.wm_title("Budget Wiz 0.1")
    main.mainloop()