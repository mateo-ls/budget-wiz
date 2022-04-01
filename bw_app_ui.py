from os import popen
from dataclasses import dataclass
from time import strftime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from tkinter import *
#from warnings import _catch_warnings_without_records
from matplotlib import offsetbox
from numpy import gradient
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
import tkinter.simpledialog
from datetime import datetime # For date object
from dateutil.relativedelta import relativedelta # For date object arithmetic

# import other tkinter files
import config
import TransactionPage
import AddTransactionPage
import EditTransactionPage
import AnalyticsPage


# Sprint 3
# TODO add labels to the add transaction page
# TODO edit transaction
# TODO add transaction
# TODO refresh category dropdown as income/expense
# TODO finish analytics UI
# TODO add custom category functionality
# TODO (low priority) delete custom category
# TODO net worth
# TODO recurring transaction
# TODO add category functionality

class MainView(tk.Tk): 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # SQLite Database Setup
        category_table = """
        create table if not exists category(
            CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            CategoryName VARCHAR(255) NOT NULL,
            Description VARCHAR(255),
            IncomeOrExpense CHAR NOT NULL,
            UNIQUE(CategoryName, IncomeOrExpense)
        );
        """
        config.cur.execute(category_table)

        recurring_table = """
        create table if not exists recurring(
            RecurrenceID INTEGER PRIMARY KEY AUTOINCREMENT,
            StartDate DATE NOT NULL,
            EndDate DATE,
            Amount DECIMAL(38,2) NOT NULL,
            Description VARCHAR(45),
            IncomeOrExpense CHAR NOT NULL, /* 'I' = Income, 'E' = Expense */
            CategoryID INT NOT NULL,
            CONSTRAINT catFK2 FOREIGN KEY (CategoryID) REFERENCES category(CategoryID)
        );
        """
        config.cur.execute(recurring_table)

        trans_table = """
        create table if not exists trans(
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            InputDate DATE NOT NULL,
            Amount DECIMAL(38,2) NOT NULL,
            Description VARCHAR(45),
            IncomeOrExpense CHAR, /* 'I' = Income, 'E' = Expense */
            RecurrenceID INT,
            CategoryID INT NOT NULL,
            CONSTRAINT recFK FOREIGN KEY (CategoryID) REFERENCES category(CategoryID),
            CONSTRAINT catFK1 FOREIGN KEY (RecurrenceID) REFERENCES recurring(RecurrenceID)
        );
        """
        config.cur.execute(trans_table)

        # DEFAULT CATEGORIES
        insert_cat = """
        insert into category (CategoryName, Description, IncomeOrExpense) values
        ("General", NULL, 'I'),
        ("Groceries", "For grocery expenses", 'E'),
        ("Bills", "For bill expenses", 'E');
        """
        
        insert_trans = """
        insert into trans values
        (001, "2022-02-16", 23.20, "Allowance", 'I', NULL, 001),
        (002, "2022-02-18", 256.99, "February groceries", 'E', NULL, 002),
        (003, "2022-02-25", 30.00, "Joe paid me back", 'I', NULL, 001),
        (004, "2022-02-28", 600.00, "February Rent", 'E', NULL, 003),
        (005, "2022-03-03", 3000.00, "Robbed local bank", 'I', NULL, 001),
        (006, "2022-04-24", 3500.00, "Feds got me", 'E', NULL, 003),
        (007, "2022-04-25", 2000.00, "Child support", 'E', NULL, 003);
        """
        try:
            config.cur.execute(insert_cat)
            config.cur.execute(insert_trans)
        except:
            pass

        # This container is where we'll stack all the frames for different pages
        # on top of each other, and the one we want to be visible will be
        # raised on top of all the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TransactionPage.TransactionPage, AddTransactionPage.AddTransactionPage, EditTransactionPage.EditTransactionPage, AnalyticsPage.AnalyticsPage):
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

    def get_page(self, page_class):
        return self.frames[page_class]    

if __name__ == "__main__":
    # At some point we can set our own custom icon
    # root.iconbitmap(default='')
    
    main = MainView()
    main.wm_geometry("800x800")
    main.wm_title("Budget Wiz 0.1")
    main.mainloop()
    
    

config.conn.commit()
#config.conn.close()