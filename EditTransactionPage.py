import bw_app_ui
import config
from AddTransactionPage import AddTransactionPage

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from tkinter import *
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
import tkinter.simpledialog
from datetime import datetime # For date object
from datetime import date
from dateutil.relativedelta import relativedelta # For date object arithmetic

class EditTransactionPage(tk.Frame):
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
        self.transactionType = StringVar()
        self.incomeRadioButton = tk.Radiobutton(self, text="Income", variable=self.transactionType, value="I")
        self.expenseRadioButton = tk.Radiobutton(self, text="Expense", variable=self.transactionType, value="E")

        # Entry fields
        self.dateCalendarEntry = DateEntry(self, width=12, background="darkblue", foreground="white", borderwidth=2)
        vcmd = (self.register(self.validateNumber))
        self.amountEntry = Entry(self, text="Amount", validate="all", validatecommand=(vcmd, '%P'))
        self.commentEntry = Entry(self, text="Comment")
        
        self.categoryOptions = [row[0] for row in config.cur.execute("select CategoryName from category;").fetchall()]
        self.categorySelected = StringVar()
        self.categoryDropdown = OptionMenu(self, self.categorySelected,*self.categoryOptions)

        # search caetgoryOptions for categorySelected
        # get index number
        # add 1 add to query

        # Submit
        submitB = tk.Button(self, text="Submit", command=lambda: self.submitButton(self.dateCalendarEntry.get_date(), self.amountEntry.get(), self.commentEntry.get(), self.transactionType.get(), self.categoryOptions, self.categorySelected.get()))
        #
        # Labels
        # TODO add labels
    
        ## Layout of above UI elements ##

        # Buttons
        transactionsButton.grid(row=0, column=0)
        addNewCategoryButton.grid(row=3, column=2)
        submitB.grid(row=7, column=1)
        self.incomeRadioButton.grid(row=1, column=1)
        self.expenseRadioButton.grid(row=1, column=2)
        reoccuringCheckbutton.grid(row=2, column=1)

        # Entry fields
        self.dateCalendarEntry.grid(row=4, column=1)
        self.amountEntry.grid(row=5, column=1)   
        self.commentEntry.grid(row=6, column=1, columnspan=2)
        self.categoryDropdown.grid(row=3, column=1)

        # Labels
        label = tk.Label(self, text="This is Edit Transaction Page")
        label.grid(row=1, column=0)
    
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
        self.UpdateTrans(date, amount, comment, type, 1, category.index(catSelect)+1)
        page = self.controller.get_page("TransactionPage")
        page.LoadIncomes(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        page.LoadExpenses(config.current_date.strftime('%m'), config.current_date.strftime('%Y'))
        self.controller.show_frame("TransactionPage")

    # function pulls and returns a tuple of all the values in the trans table
    # with global transactionID
    def PullTrans(self):
        # pull data
        query = """
        SELECT * from trans
        WHERE TransactionID = {t};
        """.format(t = config.transactionID)
        x = config.cur.execute(query).fetchall()[0]

        query2 = """
        SELECT strftime('%m', InputDate), strftime('%d', InputDate), strftime('%Y', InputDate)
        FROM trans
        WHERE TransactionID = {t};
        """.format(t = config.transactionID)
        y = config.cur.execute(query2).fetchall()[0]
        

        print(y)
        # set date
        self.dateCalendarEntry.set_date(date(month = int(y[0]), day = int(y[1]), year = int(y[2])))

        # set income or expense
        if(x[4] == 'E'):
            self.expenseRadioButton.invoke()
        elif(x[4] == 'I'):
            self.incomeRadioButton.invoke()

        # set category
        # self.categorySelected.config()

        # set recurring checkbox
        # TODO when we set up recurrence

        # set amount
        self.amountEntry.delete(0,"end")
        self.amountEntry.insert(0, x[2])

        # set description
        self.commentEntry.delete(0,"end")
        self.commentEntry.insert(0, x[3])
        
        print(x)
        
      
    def UpdateTrans(self, date, amount, desc, ioe, rid, cid):
        #print("TRANSAC: -----", config.transactionID)
        print(self.categorySelected.get())

        cid = self.categoryOptions.index(self.categorySelected.get())
        print(cid)

        query = """
        UPDATE trans
        SET 
            InputDate = "{i}", 
            Amount = {a}, 
            Description = "{d}", 
            IncomeOrExpense = '{ioe}', 
            RecurrenceID = {r},
            CategoryID = {c}
        WHERE TransactionID = {t};
        """.format(
            i = date,
            a = amount,
            d = desc,
            ioe = ioe,
            r = rid,
            c = cid,
            t = config.transactionID
        )
        print(query)
        config.cur.execute(query)
        config.conn.commit()