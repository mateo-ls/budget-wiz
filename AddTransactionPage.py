import bw_app_ui
import config

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from tkinter import *
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
import tkinter.simpledialog
from datetime import datetime # For date object
from dateutil.relativedelta import relativedelta # For date object arithmetic

class AddTransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        ## UI elements ##

        # Buttons
        transactionsButton = tk.Button(self, text="Back to Transactions", command=lambda: controller.show_frame("TransactionPage"))
        addNewCategoryButton = tk.Button(self, text="Add New Category ...", command=self.addCategory)
        todayDateButton = tk.Button(self, text="Today")
        yesterdayDateButton = tk.Button(self, text="Yesterday")
        chooseDateButton = tk.Button(self, text="Choose ...")

        # Stores boolean flag specifying if transaction is reoccurring
        # Flag as well as the onvalue/offvalue can be modified as we need
        reoccurringFlag = BooleanVar()
        reoccuringCheckbutton = tk.Checkbutton(self, text="Reoccurring Monthly?", variable=reoccurringFlag, onvalue=1, offvalue=0)

        # Stores radiobutton selection value (I or E) into transactionType string variable
        transactionType = StringVar()
        incomeRadioButton = tk.Radiobutton(self, text="Income", variable=transactionType, value="I")
        expenseRadioButton = tk.Radiobutton(self, text="Expense", variable=transactionType, value="E")

        # Entry fields
        dateCalendarEntry = DateEntry(self, width=12, background="darkblue", foreground="white", borderwidth=2)
        vcmd = (self.register(self.validateNumber))
        amountEntry = Entry(self, text="Amount", validate="all", validatecommand=(vcmd, '%P'))
        commentEntry = Entry(self, text="Comment")
        
        categoryOptions = [row[0] for row in config.cur.execute("select CategoryName from category;").fetchall()]
        print(categoryOptions)
        categorySelected = StringVar()
        categoryDropdown = OptionMenu(self, categorySelected, *categoryOptions)

        # search caetgoryOptions for categorySelected
        # get index number
        # add 1 add to query

        # Submit
        submitB = tk.Button(self, text="Submit", command=lambda: self.submitButton(dateCalendarEntry.get_date(), amountEntry.get(), commentEntry.get(), transactionType.get(), categoryOptions, categorySelected.get()))
        #
        # Labels
        # TODO add labels
        amountLabel = Label(self, text="Amount: ")
        descriptionLabel = Label(self, text="Description: ")
        categoryLabel = Label(self, text="Category: ")
    
        ## Layout of above UI elements ##

        # Buttons
        transactionsButton.grid(row=0, column=0)
        addNewCategoryButton.grid(row=3, column=2)
        submitB.grid(row=7, column=1)
        incomeRadioButton.grid(row=1, column=1)
        expenseRadioButton.grid(row=1, column=2)
        reoccuringCheckbutton.grid(row=2, column=1)

        # Entry fields
        dateCalendarEntry.grid(row=4, column=1)
        amountEntry.grid(row=5, column=1)   
        commentEntry.grid(row=6, column=1, columnspan=2)
        categoryDropdown.grid(row=3, column=1)

        # Labels
        amountLabel.grid(row=5, column=0)
        categoryLabel.grid(row=3, column=0)
        descriptionLabel.grid(row=6, column=0)

    
    # Should run when addNewCategoryButton is pressed
    def addCategory(event = None):
        # TODO pull category field
        # TODO INSERT into category table
        # answer = AddCategoryDialog()
        global pop
        pop = Toplevel(bw_app_ui.main)
        pop.title("Add New Category")
        pop.geometry("500x350")
        transactionType = StringVar()
        tk.Radiobutton(pop, text="Income", variable=transactionType, value="I").grid(row=0, column=0)
        tk.Radiobutton(pop, text="Expense", variable=transactionType, value="E").grid(row=0, column=1)

        tk.Label(pop, text="Name:").grid(row=1, column=0)
        categoryNameEntry = Entry(pop)
        categoryNameEntry.grid(row=1, column=1, columnspan=2)

        tk.Label(pop, text="Description:").grid(row=2, column=0)
        categoryDescriptionEntry = Entry(pop)
        categoryDescriptionEntry.grid(row=2, column=1, columnspan=2)

        addCategorySubmitButton = tk.Button(pop, text="Submit",
         command=lambda: [AddTransactionPage.submitCategory(transactionType.get(), categoryNameEntry.get(),
          categoryDescriptionEntry.get()), pop.destroy()])
        addCategorySubmitButton.grid(row=3, column=1)

    # Should run when submitButton() is pressed
    def submitTransaction(self, date, amount, desc, ioe, rid, cid):
        # TODO check that all fields have a value
        # TODO if recurring button is pressed, INSERT into recurring table
        
        # query
        transaction = """
        INSERT into trans (InputDate, Amount, Description, IncomeOrExpense, RecurrenceID, CategoryID)
        values (?, ?, ?, ?, ?, ?);
        """

        values = (date, amount, desc, ioe, rid, cid)
        config.cur.execute(transaction, values)
        config.conn.commit()


    def submitCategory(transactionType, Name, Description):
        # TODO insert
        print(transactionType)
        print(Name)
        print(Description)
        return
    
    def validateNumber(self, P):
        if str.isdigit(P) or str(P) == "":
            return True
        else:
            return False

    def submitButton(self, date, amount, comment, type, category, catSelect):
        self.submitTransaction(date, amount, comment, type, 1, category.index(catSelect)+1)
        page = self.controller.get_page("TransactionPage")
        page.LoadIncomes(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        page.LoadExpenses(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        self.controller.show_frame("TransactionPage")