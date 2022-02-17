import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
# Need to import and setup mySQL database


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
        
        selfButton = tk.Button(self, text="Transactions")
        analyticsButton = tk.Button(self, text="Analytics")
        addButton = tk.Button(self, text="Add", command=lambda: controller.show_frame("AddTransactionPage"))
        editButton = tk.Button(self, text="Edit")
        deleteButton = tk.Button(self, text="Delete")

        selfButton.grid(row=0, column=0)
        analyticsButton.grid(row=0, column=1)
        deleteButton.grid(row=0, column=10)
        editButton.grid(row=0, column=9)
        addButton.grid(row=0, column=8)

        label = tk.Label(self, text="This is Transaction Page")
        label.grid(row=5, column=5)
       

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
        

if __name__ == "__main__":
    # At some point we can set our own custom icon
    # root.iconbitmap(default='')
    
    main = MainView()
    main.wm_geometry("800x800")
    main.wm_title("Budget Wiz 0.1")
    main.mainloop()