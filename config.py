
# sqlite database connection
import sqlite3
conn = sqlite3.connect('dw_data.db')
cur = conn.cursor()

# ----- Establish Global Variable for Current Date -----
# Link: https://www.w3schools.com/python/python_datetime.asp
# store current date across files
from datetime import datetime # For date object
from dateutil.relativedelta import relativedelta # For date object arithmetic
current_date = datetime.now()

# transactionID stores selected field
transactionID = 1