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
        

        ###### UI elements ######

        # Buttons
        transactionsButton = tk.Button(self, text="Back to Transactions", command=lambda: controller.show_frame("TransactionPage"))
        addNewCategoryButton = tk.Button(self, text="Add New Category ...", command=self.addCategory)
        todayDateButton = tk.Button(self, text="Today")
        yesterdayDateButton = tk.Button(self, text="Yesterday")
        chooseDateButton = tk.Button(self, text="Choose ...")

        # Stores boolean flag specifying if transaction is reoccurring
        # Flag as well as the onvalue/offvalue can be modified as we need
        self.reoccurringFlag = BooleanVar()
        reoccuringCheckbutton = tk.Checkbutton(self, text="Reoccurring Monthly?", variable=self.reoccurringFlag, onvalue=1, offvalue=0)


        # ----- Category Options Dropdown -----
        categoryOptions = [row[0] for row in config.cur.execute(
            "select CategoryName from category where IncomeOrExpense = 'I';").fetchall()]
            # This sets the default categories to Income (check Radiobutton section below)
        print(categoryOptions)
        self.categorySelected = StringVar()
        self.categoryDropdown = tk.OptionMenu(
            self, 
            self.categorySelected, 
            *categoryOptions
        )


        # ----- Radiobutton Selection (I or E) -----
        # Default radiobutton selected will be 'I'. Therefore, changeCategoryOption will run as 'I' First
        transactionType = StringVar(None, 'I') # Sets default of string var transactionType = 'I'
        incomeRadioButton = tk.Radiobutton(
            self, 
            text="Income", 
            variable=transactionType, 
            value='I',
            command=lambda:[
                self.setCategoryOption('I')
            ]
        )
        expenseRadioButton = tk.Radiobutton(
            self, 
            text="Expense", 
            variable=transactionType, 
            value='E',
            command=lambda:[
                self.setCategoryOption('E')
            ]
        )

        # Entry fields
        dateCalendarEntry = DateEntry(self, width=12, background="darkblue", foreground="white", borderwidth=2)
        vcmd = (self.register(self.validateNumber))
        amountEntry = Entry(self, text="Amount", validate="all", validatecommand=(vcmd, '%P'))
        commentEntry = Entry(self, text="Comment")

        # search caetgoryOptions for self.categorySelected
        # get index number
        # add 1 add to query

        # Submit
        submitB = tk.Button(self, text="Submit", command=lambda: self.submitButton(dateCalendarEntry.get_date(), amountEntry.get(), commentEntry.get(), transactionType.get(), categoryOptions, self.categorySelected.get()))
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
        self.submitB.grid(row=7, column=1)
        incomeRadioButton.grid(row=1, column=1)
        expenseRadioButton.grid(row=1, column=2)
        reoccuringCheckbutton.grid(row=2, column=1)

        # Entry fields
        dateCalendarEntry.grid(row=4, column=1)
        amountEntry.grid(row=5, column=1)   
        commentEntry.grid(row=6, column=1, columnspan=2)
        self.categoryDropdown.grid(row=3, column=1)

        # Labels
        amountLabel.grid(row=5, column=0)
        categoryLabel.grid(row=3, column=0)
        descriptionLabel.grid(row=6, column=0)

    def validateSubmit(self, *args):
        a = self.transactionType.get()
        b = self.amountVar.get()
        c = self.commentVar.get()
        d = self.categorySelected.get()
        if a and b and c and d:
            self.submitB.config(state='normal')
        else:
            self.submitB.config(state='disabled')
    
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
        print(values)
        config.cur.execute(transaction, values)
        config.conn.commit()

    def submitCategory(transactionType, Name, Description):
        # TODO insert
        print(transactionType)
        print(Name)
        print(Description)
        return

    def resetCategoryOption(self, options, index=None):
        # Reset the dropdown menu
        menu = self.categoryDropdown["menu"]
        menu.delete(0, "end")

        for string in options:
            menu.add_command(
                label=string,
                command=lambda value=string:
                    self.categorySelected.set(value)
        )
        
        if index is not None:
            self.categorySelected.set(options[index])

    def setCategoryOption(self, option):
        # option will be either 'I' or 'E'
        grab_categories = """
        select CategoryName from category where IncomeOrExpense = '{x}';
        """.format(x = option)
        categoryOptions = [row[0] for row in config.cur.execute(grab_categories).fetchall()]
        self.resetCategoryOption(categoryOptions, 0)
    
    def validateNumber(self, P):
        if str.isdigit(P) or str(P) == "":
            return True
        else:
            return False

    def submitButton(self, date, amount, comment, type, category, catSelect):
        query = """
        select CategoryID from category
        where CategoryName = "{cat}"
        """.format(cat = catSelect)

        cid = config.cur.execute(query).fetchall()[0][0]

        self.submitTransaction(date, amount, comment, type, 1, cid)
        page = self.controller.get_page("TransactionPage")
        page.LoadIncomes(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        page.LoadExpenses(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        self.controller.show_frame("TransactionPage")
        # Calculate new net worth based off added transaction
        page.calculateNetWorth("month")
        page.calculateNetWorth("total")