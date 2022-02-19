import subprocess
# subprocess.call(['pip', 'install', 'mysql.connector'])

import mysql.connector as mysqlc

# connect to database
db_con = mysqlc.connect(host="localhost", user="root", password="", database="budgetwiz")
db_cursor = db_con.cursor(buffered=True) # cursor holds current spot

# get income transactions
query1 = "select TransactionID, InputDate, transaction.Description, Amount, CategoryName from transaction inner join category using (CategoryID) where IncomeOrExpense = 'I'"
db_cursor.execute(query1)
incomes = db_cursor.fetchall()

# get expense transactions
query2 = "select TransactionID, InputDate, transaction.Description, Amount, CategoryName from transaction inner join category using (CategoryID) where IncomeOrExpense = 'E'"
db_cursor.execute(query2)
expenses = db_cursor.fetchall()