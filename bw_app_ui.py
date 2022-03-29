from os import popen
from dataclasses import dataclass
from time import strftime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from tkinter import *
#from warnings import _catch_warnings_without_records
from matplotlib import offsetbox
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk
import tkinter.simpledialog
from datetime import datetime # For date object
from dateutil.relativedelta import relativedelta # For date object arithmetic

# connect to SQLite Database
import sqlite3
conn = sqlite3.connect('dw_data.db')
cur = conn.cursor()

update = True

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
        cur.execute(category_table)

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
        cur.execute(recurring_table)

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
        cur.execute(trans_table)

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
            cur.execute(insert_cat)
        except:
            pass
        # cur.execute(insert_trans)

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

    def get_page(self, page_class):
        return self.frames[page_class]

# ----- Establish Global Variable for Current Date -----
# Link: https://www.w3schools.com/python/python_datetime.asp
current_date = datetime.now()

class TransactionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        # Establishes this pages UI elements/
        # Date, description, amount, category


        # ----- Buttons -----
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
            text="Edit"
        )
        deleteButton = tk.Button(self, text="Delete")
        thisMonthButton = tk.Button(self, text="This Month")
        

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
        month_and_year = f"{current_date.strftime('%B')} {current_date.strftime('%Y')}"
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


        # ----- Other Labels -----
        incomeLabel = tk.Label(self, text="Incomes")
        expenseLabel = tk.Label(self, text="Expenses")
        label = tk.Label(self, text="This is Transaction Page")

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
        self.tvIncomes.bind("<<TreeviewSelect>>", self.selectRecordIncome)

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
        self.tvExpenses.bind("<<TreeviewSelect>>", self.selectRecordExpense)


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

        # Image Buttons
        leftArrowButton.grid(row=1, column=1)
        rightArrowButton.grid(row=1, column=3)

        # Labels
        self.selectedMonthLabel.grid(row=1, column=2)
        incomeLabel.grid(row=2, column=2)
        expenseLabel.grid(row=2, column=5)
        label.grid(row=5, column=5)

        # Treeviews
        self.tvIncomes.grid(row=3, column=1, columnspan=3)
        self.tvExpenses.grid(row=3, column=5, columnspan=3)

        # These two are needed for the initial loading to the Transactions Page
        self.LoadIncomes(current_date.strftime('%m'), current_date.strftime('%Y'))
        self.LoadExpenses(current_date.strftime('%m'), current_date.strftime('%Y'))


        # Sets minimun sizes for all columns or rows
        # Might want to change/get rid of this later
        #columnCount, rowCount = self.grid_size()
        #for column in range(columnCount):
        #    self.grid_columnconfigure(column, minsize=100)
        #for row in range(rowCount):
        #    self.grid_rowconfigure(row, minsize=100)
    
    def changeMonth(self, direction):
        global current_date # Establish that the current_data global var will be used here

        if direction == "left":
            current_date = current_date - relativedelta(months=1)
        elif direction == "right":
            current_date = current_date + relativedelta(months=1)
        else: 
            current_date = datetime.now()

        # Update the selectedMonthLabel and Incomes & Expenses Table
        m_y = f"{current_date.strftime('%B')} {current_date.strftime('%Y')}"
        self.selectedMonthLabel["text"] = m_y
        self.LoadIncomes(current_date.strftime('%m'), current_date.strftime('%Y'))
        self.LoadExpenses(current_date.strftime('%m'), current_date.strftime('%Y'))


    def selectRecordIncome(self, event):
        global transactionID
        transactionID = self.tvIncomes.selection()[0]
        return transactionID
    
    def selectRecordExpense(self, event):
        global transactionID
        transactionID = self.tvExpenses.selection()[0]
        return transactionID

    
    # When called, loads Income data from database into tvIncomes
    def LoadIncomes(self, month, year):
        # TODO Ensure connection to database here
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

        rows = cur.execute(income).fetchall()
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

        rows = cur.execute(expenses).fetchall()
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
        
        categoryOptions = [row[0] for row in cur.execute("select CategoryName from category;").fetchall()]
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
        label = tk.Label(self, text="This is Add Transaction Page")
        label.grid(row=1, column=0)

    
    # Should run when addNewCategoryButton is pressed
    def addCategory(event = None):
        # TODO pull category field
        # TODO INSERT into category table
        # answer = AddCategoryDialog()
        global pop
        pop = Toplevel(main)
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
        cur.execute(transaction, values)
        conn.commit()


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
        page.LoadIncomes(current_date.strftime('%m'), current_date.strftime('%Y'))
        page.LoadExpenses(current_date.strftime('%m'), current_date.strftime('%Y'))
        self.controller.show_frame("TransactionPage")

class EditTransactionPage(tk.Frame):
    # TODO setup UI elements
    # TODO load selected transaction
    # TODO model add transaction, but with UPDATE command
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # label.pack(side="top", fill="both", expand=True)
        
        ## UI Elements ##

        #Buttons
        transactionsButton = tk.Button(self, text="Back to Transactions", command=lambda: controller.show_frame("TransactionPage"))
        
        # Labels
        label = tk.Label(self, text="This is Edit Transaction Page")

        ## Layout of above UI elements ##

        # Buttons
        transactionsButton.grid(row=0, column=0)

        # Labels
        label.grid(row=1, column=0)

class AnalyticsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #label.pack(side="top", fill="both", expand=True)

        transactionsButton = tk.Button(self, text="Back to Transactions", command=lambda: controller.show_frame("TransactionPage"))
        
        # Labels
        label = tk.Label(self, text="This is Analytics Page")

        ## Layout of above UI elements ##

        # Buttons
        transactionsButton.grid(row=0, column=0)

        # Labels
        label.grid(row=1, column=0)

        arrowImage = Image.open('resources/arrow_icon.png')
        arrowImage = arrowImage.resize((30, 30), Image.ANTIALIAS)
        arrowImageFlipped = Image.open('resources/arrow_icon_flipped.png')
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
    
    

conn.commit()
conn.close()