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
import calendar
from dateutil.relativedelta import relativedelta # For date object arithmetic

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Buttons
        selfButton = tk.Button(
            self, 
            text="Transactions", 
            command=lambda: controller.show_frame("TransactionPage"))
        analyticsButton = tk.Button(self, text="Analytics")

        thisMonthButton = tk.Button(self, text="This Month")
        
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

        # Labels

        # Categories Treeview
        columns = ("#1", "#2")
        self.tvCategoryTotals = ttk.Treeview(self, show="headings", height="5", columns=columns)
        self.tvCategoryTotals.heading("#1", text="Category", anchor="center")
        self.tvCategoryTotals.column("#1", width=80, anchor="center", stretch=True)
        self.tvCategoryTotals.heading("#2", text="Amount", anchor="center")
        self.tvCategoryTotals.column("#2", width=80, anchor="center", stretch=True)
        
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tvCategoryTotals.yview)
        self.tvCategoryTotals.configure(yscroll=vsb.set)
        # Don't know if we need to select anything for this treeview
        # self.tvCategoryTotals.bind("<<TreeviewSelect>>", s)

        # Charts
        self.plotGraph()

        # figure2 = plt.Figure(figsize=(4,3), dpi=100)
        # ax2 = figure2.add_subplot(111)
        # chart_type2 = FigureCanvasTkAgg(figure2, self)
        # chart_type2.get_tk_widget().grid(row=4, column=6)
        # df2 = df2[['First Column','Second Column']].groupby('First Column').sum()
        # df2.plot(kind='CHART TYPE', legend=True, ax=ax2)
        # ax2.set_title('CHART TITLE')


        ## Layout

        # Buttons
        selfButton.grid(row=0, column=0)
        analyticsButton.grid(row=0, column=1)
        thisMonthButton.grid(row=1, column=5)

        # Image Buttons
        leftArrowButton.grid(row=1, column=1)
        rightArrowButton.grid(row=1, column=3)

        # Labels
        self.selectedMonthLabel.grid(row=1, column=2)

        # Treeviews
        self.tvCategoryTotals.grid(row=3, column=1, columnspan=3, rowspan=2)
    
    def changeMonth(self, direction):
        if direction == "left": # If left arrow is pressed (go back a month)
            config.current_date = config.current_date - relativedelta(months=1)
        elif direction == "right": # If right arrow is pressed (go forward a month)
            config.current_date = config.current_date + relativedelta(months=1)
        else: 
            config.current_date = datetime.now()

        # Update the selectedMonthLabel and Incomes & Expenses Table
        m_y = f"{config.current_date.strftime('%B')} {config.current_date.strftime('%Y')}"
        self.selectedMonthLabel["text"] = m_y
        # This is where we'll need to update the category box and the graphs
        # Clears the dataframe
        # self.df1 = self.df1[0:0]
        # days = range(1, calendar.monthrange(config.current_date.year, config.current_date.month)[1])
        # for d in days:
        #     self.df1 = self.df1.append({'Day': d, 'Net Worth': self.calculateDayNetWorth(d)}, ignore_index=TRUE)
        # self.df1.plot(x = 'Day', y = 'Net Worth', kind='line', legend=True, ax=self.ax1)
        self.plotGraph()
    
    def calculateDayNetWorth(self, day):
        month = config.current_date.strftime('%m')
        year = config.current_date.strftime('%Y')

        grab_income = """
        select sum(Amount)
        from trans 
        where IncomeOrExpense='I' and
        strftime('%m', trans.InputDate) = '{m}' and
        strftime('%Y', trans.InputDate) = '{y}' and
        cast(strftime('%d', trans.InputDate) as decimal) <= {d} ;
        """.format(m = month, y = year, d = day)

        grab_expense = """
        select sum(Amount)
        from trans 
        where IncomeOrExpense='E' and
        strftime('%m', trans.InputDate) = '{m}' and
        strftime('%Y', trans.InputDate) = '{y}' and
        cast(strftime('%d', trans.InputDate) as decimal) <= {d} ;
        """.format(m = month, y = year, d = day)
        print(grab_expense)

        total_income = 0
        total_expense = 0

        # Fetch total income and expenses from their respective queries
        total_income_list = config.cur.execute(grab_income).fetchall()
        if total_income_list[0][0] != None: # If there are no income entries for that month,
            # the query will return a list with a None element (same goes for expenses)
            total_income = total_income_list[0][0]
        else:
            total_income = 0
            
        total_expense_list = config.cur.execute(grab_expense).fetchall()
        if total_expense_list[0][0] != None:
            total_expense = total_expense_list[0][0]
        else:
            total_expense = 0

        net_worth = round(total_income - total_expense, 2)

        return net_worth

    def plotGraph(self):
        self.figure1 = plt.Figure(figsize=(4,3), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        chart_type1 = FigureCanvasTkAgg(self.figure1, self)
        chart_type1.get_tk_widget().grid(row=3, column=6)
        # This is where you define the dataframe to plot
        #df1 = df1[['First Column','Second Column']].groupby('First Column').sum()
        self.df1 = pd.DataFrame(columns=['Day', 'Month Net Worth'])
        days = range(1, calendar.monthrange(config.current_date.year, config.current_date.month)[1])
        for d in days:
            self.df1 = self.df1.append({'Day': d, 'Month Net Worth': self.calculateDayNetWorth(d)}, ignore_index=TRUE)
        self.df1.plot(x = 'Day', y = 'Month Net Worth', kind='line', legend=True, ax=self.ax1)
        self.ax1.set_title('Month Net Worth by Day')
