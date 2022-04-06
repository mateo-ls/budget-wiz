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

from pandas import DataFrame
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
        # figure1 = plt.Figure(figsize=(4,3), dpi=100)
        # ax1 = figure1.add_subplot(111)
        # chart_type1 = FigureCanvasTkAgg(figure1, self)
        # chart_type1.get_tk_widget().grid(row=3, column=6)
        # df1 = df1[['First Column','Second Column']].groupby('First Column').sum()
        # df1.plot(kind='CHART TYPE', legend=True, ax=ax1)
        # ax1.set_title('CHART TITLE')

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