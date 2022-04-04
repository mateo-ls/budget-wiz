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
        ("General Income", NULL, 'I'),
        ("General Expenses", NULL, 'E'),
        ("Groceries", "Grocery expenses", 'E'),
        ("Outside Dining", "Expenses from outside dining", 'E'),
        ("Bills", "Bill expenses", 'E'),
        ("Gaming", "Expenses related to gaming", 'E'),
        ("School", "School expenses", 'E'),
        ("Work", "Work income", 'I'),
        ("Stocks", "Income from stocks", 'I'),
        ("Winnings", "Income from tournament winnings", 'I');
        """
        
        insert_trans = """
        insert into trans values
        (001, "2022-02-01", 2400.00, "Child support", 'E', NULL, 002),
        (002, "2022-02-04", 256.99, "Groceries", 'E', NULL, 003),
        (003, "2022-02-10", 30.00, "Joe paid me back", 'I', NULL, 001),
        (004, "2022-02-11", 900.00, "Monthly rent paid", 'E', NULL, 005),
        (005, "2022-02-12", 3000.00, "Allowance", 'I', NULL, 001),
        (006, "2022-02-16", 3500.00, "Found the imposter", 'I', NULL, 008),
        (008, "2022-02-20", 5445.45, "College Tuition Payment 1/3", 'E', NULL, 007),
        (009, "2022-02-25", 94.00, "Groceries", 'E', NULL, 003),
        (010, "2022-02-28", 240.00, "Dogecoin earnings", 'I', NULL, 009),
        (011, "2022-03-01", 2400.00, "Child support", 'E', NULL, 002),
        (012, "2022-03-02", 540.99, "New gaming PC", 'E', NULL, 006),
        (013, "2022-03-05", 1500.00, "Fixed wires in electrical", 'I', NULL, 008),
        (014, "2022-03-10", 900.00, "Monthly rent paid", 'E', NULL, 005),
        (015, "2022-03-13", 1500.00, "Won local hotdog-eating tournament", 'I', NULL, 010),
        (016, "2022-03-13", 140.00, "Dogecoin earnings", 'I', NULL, 009),
        (017, "2022-03-14", 3483.80, "College Tuition Payment 2/3", 'E', NULL, 007),
        (018, "2022-03-16", 235.89, "Groceries", 'E', NULL, 003),
        (019, "2022-03-19", 456.70, "Groceries", 'E', NULL, 003),
        (020, "2022-03-25", 45.90, "Paid my homie back for venting", 'E', NULL, 002),
        (021, "2022-03-25", 3000.00, "AMONGUS", 'I', NULL, 001),
        (022, "2022-03-30", 15.00, "McDonalds", 'E', NULL, 004),
        (023, "2022-03-31", 4750.00, "Found the imposrter", 'I', NULL, 008),
        (024, "2022-04-01", 2400.00, "Child support", 'E', NULL, 002),
        (025, "2022-04-04", 3000.00, "Dogecoin earnings", 'I', NULL, 009),
        (026, "2022-04-06", 147.00, "Groceries", 'E', NULL, 003),
        (027, "2022-04-06", 24.98, "Taco Bell", 'E', NULL, 004),
        (028, "2022-04-11", 900.00, "Montly rent paid", 'E', NULL, 003),
        (029, "2022-04-12", 2200.00, "Fixed my AMONGUS car", 'E', NULL, 002),
        (030, "2022-04-17", 400.00, "Won local Big Chungus tournament", 'I', NULL, 010),
        (031, "2022-04-19", 13.90, "McDonald", 'E', NULL, 004),
        (032, "2022-04-23", 2767.55, "College Tuition Payment 3/3", 'E', NULL, 007),
        (033, "2022-04-24", 6969.69, "Purchased AMONGUS", 'E', NULL, 006),
        (034, "2022-04-26", 87.80, "Groceries", 'E', NULL, 003);
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