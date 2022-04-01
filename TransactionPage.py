import bw_app_ui
import config

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from tkinter import *
from PIL import Image, ImageTk
import tkinter.simpledialog
from datetime import datetime # For date object
from dateutil.relativedelta import relativedelta # For date object arithmetic

class TransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        # Establishes this pages UI elements/
        # Date, description, amount, category


        # ----- Navigation and Add/Edit/Delete Buttons -----
        selfButton = tk.Button(self, text="Transactions")
        analyticsButton = tk.Button(
            self, 
            text="Analytics", 
            command=lambda: controller.show_frame("AnalyticsPage")
        )
        addButton = tk.Button(
            self,
            text="Add", 
            command=lambda: controller.show_frame("AddTransactionPage")
        )
        editButton = tk.Button(
            self, 
            text="Edit",
            command=lambda: controller.show_frame("EditTransactionPage")
        )
        deleteButton = tk.Button(self, text="Delete")
        

        # ----- Upload Images for Left and Right Arrows -----
        # Getting this to work was really dumb
        # Let's stay away from image UI elements
        arrowImage = Image.open('resources/arrow_icon.png')
        arrowImage = arrowImage.resize((30, 30), Image.ANTIALIAS)
        arrowImageFlipped = Image.open('resources/arrow_icon_flipped.png')
        arrowImageFlipped = arrowImageFlipped.resize((30, 30), Image.ANTIALIAS)
        arrowIcon = ImageTk.PhotoImage(arrowImage)
        arrowIconFlipped = ImageTk.PhotoImage(arrowImageFlipped)


        # ----- Month Selection Buttons and Labels ----- 
        month_and_year = f"{config.current_date.strftime('%B')} {config.current_date.strftime('%Y')}"
        self.selectedMonthLabel = tk.Label(self, text=month_and_year)

        leftArrowButton = tk.Button(
            self,
            image=arrowIcon,
            borderwidth=0,
            command=lambda: self.changeMonth("left")
        )
        leftArrowButton.image = arrowIcon

        rightArrowButton = tk.Button(
            self, 
            image=arrowIconFlipped, 
            borderwidth=0,
            command=lambda: self.changeMonth("right")
        )
        rightArrowButton.image = arrowIconFlipped

        thisMonthButton = tk.Button(
            self, 
            text="This Month",
            command=lambda: self.changeMonth("current")
        )

        # ----- Networth Button and Label -----
        calculateNetWorth = tk.Button(
            self,
            text="Networth",
            command=lambda: self.calculateNetWorth()

        )
        netWorth = tk.Label(
            self
        )

        # ----- Other Labels -----
        incomeLabel = tk.Label(self, text="Incomes")
        expenseLabel = tk.Label(self, text="Expenses")

        # Incomes Treeview
        columns = ("#1", "#2", "#3", "#4")
        self.tvIncomes = ttk.Treeview(self, show="headings", height="5", columns=columns)
        # Do we want a column for TransactionID?
        self.tvIncomes.heading("#1", text="Date", anchor="center")
        self.tvIncomes.column("#1", width=80, anchor="center",stretch=True)
        self.tvIncomes.heading("#2", text="Description", anchor="center")
        self.tvIncomes.column("#2", width=80, anchor="center",stretch=True)
        self.tvIncomes.heading("#3", text="Amount", anchor="center")
        self.tvIncomes.column("#3", width=80, anchor="center",stretch=True)
        self.tvIncomes.heading("#4", text="Category", anchor="center")
        self.tvIncomes.column("#4", width=80, anchor="center",stretch=True)

        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tvIncomes.yview)
        # TODO Need to place vertical scroll bar using either grid or place
        # We'll figure that out later
        self.tvIncomes.configure(yscroll=vsb.set)
        self.tvIncomes.bind("<ButtonRelease-1>", self.selectRecordIncome)

        # Expenses Treeview
        columns = ("#1", "#2", "#3", "#4")
        self.tvExpenses = ttk.Treeview(self, show="headings", height="5", columns=columns)
        # Do we want a column for TransactionID?
        self.tvExpenses.heading("#1", text="Date", anchor="center")
        self.tvExpenses.column("#1", width=80, anchor="center",stretch=True)
        self.tvExpenses.heading("#2", text="Description", anchor="center")
        self.tvExpenses.column("#2", width=80, anchor="center",stretch=True)
        self.tvExpenses.heading("#3", text="Amount", anchor="center")
        self.tvExpenses.column("#3", width=80, anchor="center",stretch=True)
        self.tvExpenses.heading("#4", text="Category", anchor="center")
        self.tvExpenses.column("#4", width=80, anchor="center",stretch=True)

        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tvExpenses.yview)
        # TODO Need to place vertical scroll bar using either grid or place
        # We'll figure that out later
        self.tvExpenses.configure(yscroll=vsb.set)
        self.tvExpenses.bind("<ButtonRelease-1>", self.selectRecordExpense)


        # ----- Establishes layout of above elements -----
        # This is bad
        # TODO make it pretty
        # Buttons
        selfButton.grid(row=0, column=0)
        analyticsButton.grid(row=0, column=1)
        deleteButton.grid(row=0, column=7)
        editButton.grid(row=0, column=6)
        addButton.grid(row=0, column=5)
        thisMonthButton.grid(row=1, column=5)

        calculateNetWorth.grid(row=1, column=6) # <- This is temporary

        # Image Buttons
        leftArrowButton.grid(row=1, column=1)
        rightArrowButton.grid(row=1, column=3)

        # Labels
        self.selectedMonthLabel.grid(row=1, column=2)
        incomeLabel.grid(row=2, column=2)
        expenseLabel.grid(row=2, column=5)

        # Treeviews
        self.tvIncomes.grid(row=3, column=1, columnspan=3)
        self.tvExpenses.grid(row=3, column=5, columnspan=3)

        # These two are needed for the initial loading to the Transactions Page
        self.LoadIncomes(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        self.LoadExpenses(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))


        # Sets minimun sizes for all columns or rows
        # Might want to change/get rid of this later
        #columnCount, rowCount = self.grid_size()
        #for column in range(columnCount):
        #    self.grid_columnconfigure(column, minsize=100)
        #for row in range(rowCount):
        #    self.grid_rowconfigure(row, minsize=100)
    
    def changeMonth(self, direction):
        if direction == "left":
            config.current_date = config.current_date - relativedelta(months=1)
        elif direction == "right":
            config.current_date = config.current_date + relativedelta(months=1)
        else: 
            config.current_date = datetime.now()

        # Update the selectedMonthLabel and Incomes & Expenses Table
        m_y = f"{config.current_date.strftime('%B')} {config.current_date.strftime('%Y')}"
        self.selectedMonthLabel["text"] = m_y
        self.LoadIncomes(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        self.LoadExpenses(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))


    def selectRecordIncome(self, event):
        curItem = self.tvIncomes.identify('item', event.x, event.y)
        config.transactionID = self.tvIncomes.item(curItem, "text")
        #print(config.transactionID)
    
    def selectRecordExpense(self, event):
        curItem = self.tvExpenses.identify('item', event.x, event.y)
        print(curItem)
        config.transactionID = self.tvExpenses.item(curItem, "text")
        print(config.transactionID)
        #print(config.transactionID)

    def calculateNetWorth(self, **kwargs):
        option = ""

        if option == 'month': # For by-month net worth
            month = config.current_date.strftime('%m')
            year = config.current_date.strftime('%Y')

            grab_income = """
            select sum(Amount)
            from trans 
            where IncomeOrExpense='I'
            and month(InputDate)={m}
            and year(InputDate)={y};
            """.format(m = month, y = year)

            grab_expense = """
            select sum(Amount) 
            from trans 
            where IncomeOrExpense='E'            
            and month(InputDate)={m}
            and year(InputDate)={y};
            """.format(m = month, y = year)
        else: # For total net worth
            grab_income = """
            select sum(Amount)
            from trans 
            where IncomeOrExpense='I';
            """

            grab_expense = """
            select sum(Amount) 
            from trans 
            where IncomeOrExpense='E';
            """

        total_income_list = config.cur.execute(grab_income).fetchall()
        total_expense_list = config.cur.execute(grab_expense).fetchall()
        
        total_income = 0
        total_expense = 0

        for x in total_income_list:
            total_income = x[0]

        for x in total_expense_list:
            total_expense = x[0]

        net_worth = total_income - total_expense
        print(net_worth)
    
    # When called, loads Income data from database into tvIncomes
    def LoadIncomes(self, month, year):
        # Clears the treeview tvIncomes
        self.tvIncomes.delete(*self.tvIncomes.get_children())
        
        income = """
        select TransactionID, InputDate, trans.Description, Amount, CategoryName 
        from trans 
        inner join category using (CategoryID) 
        where trans.IncomeOrExpense = 'I' and
        strftime('%m', trans.InputDate) = '{m}' and 
        strftime('%Y', trans.InputDate) = '{y}'
        """.format(m = month, y = year)

        rows = config.cur.execute(income).fetchall()
        TransactionID = ""
        Date = ""
        Description = ""
        Amount = ""
        Category = ""
        for row in rows:
            TransactionID = row[0]
            Date = row[1]
            Description = row[2]
            Amount = row[3]
            Category = row[4]
            self.tvIncomes.insert("", 'end', text=TransactionID, values=(Date, Description, Amount, Category))

    # When called, loads Expense data from database into tvExpenses
    def LoadExpenses(self, month, year):
        # Clears the treeview tvExpenses
        self.tvExpenses.delete(*self.tvExpenses.get_children())
        
        expenses = """
        select TransactionID, InputDate, trans.Description, Amount, CategoryName 
        from trans 
        inner join category using (CategoryID) 
        where trans.IncomeOrExpense = 'E' and
        strftime('%m', trans.InputDate) = '{m}' and
        strftime('%Y', trans.InputDate) = '{y}'
        """.format(m = month, y = year)

        rows = config.cur.execute(expenses).fetchall()
        TransactionID = ""
        Date = ""
        Description = ""
        Amount = ""
        Category = ""
        for row in rows:
            TransactionID = row[0]
            Date = row[1]
            Description = row[2]
            Amount = row[3]
            Category = row[4]
            self.tvExpenses.insert("", 'end', text=TransactionID, values=(Date, Description, Amount, Category))