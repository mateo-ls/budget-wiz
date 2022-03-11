# import subprocess
# subprocess.call(['pip', 'install', 'mysql.connector'])

# import mysql.connector as mysqlc

# connect to database
# db_con = mysqlc.connect(host="localhost", user="root", password="", database="budgetwiz")
# db_cursor = db_con.cursor(buffered=True) # cursor holds current spot

# get income transactions
# query1 = "select TransactionID, InputDate, transaction.Description, Amount, CategoryName from transaction inner join category using (CategoryID) where IncomeOrExpense = 'I'"
# db_cursor.execute(query1)
# incomes = db_cursor.fetchall()

# get expense transactions
# query2 = "select TransactionID, InputDate, transaction.Description, Amount, CategoryName from transaction inner join category using (CategoryID) where IncomeOrExpense = 'E'"
# db_cursor.execute(query2)
# expenses = db_cursor.fetchall()

########################
## SQLite Sample Code ##
########################

import sqlite3
conn = sqlite3.connect('dw_data.db')
cur = conn.cursor()

# initial database creation (with if conditions to uphold data integrity)
category_table = """
create table if not exists category(
    CategoryID INT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    Description VARCHAR(255),
    IncomeOrExpense CHAR NOT NULL,
    CONSTRAINT catPK PRIMARY KEY (CategoryID)
);
"""

recurring_table = """
create table if not exists recurring(
    RecurrenceID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Amount DECIMAL(38,2) NOT NULL,
    Description VARCHAR(45),
    IncomeOrExpense CHAR NOT NULL, /* 'I' = Income, 'E' = Expense */
    CategoryID INT NOT NULL,
    CONSTRAINT recPK PRIMARY KEY (RecurrenceID),
    CONSTRAINT catFK2 FOREIGN KEY (CategoryID) REFERENCES category(CategoryID)
);
"""

trans_table = """
create table if not exists trans(
    TransactionID INT NOT NULL,
    InputDate DATE NOT NULL,
    Amount DECIMAL(38,2) NOT NULL,
    Description VARCHAR(45),
    IncomeOrExpense CHAR, /* 'I' = Income, 'E' = Expense */
    RecurrenceID INT,
    CategoryID INT NOT NULL,
    CONSTRAINT transPK PRIMARY KEY (TransactionID),
    CONSTRAINT recFK FOREIGN KEY (CategoryID) REFERENCES category(CategoryID),
    CONSTRAINT catFK1 FOREIGN KEY (RecurrenceID) REFERENCES recurring(RecurrenceID)
);
"""

insert_cat = """
insert into category values
(001, "General", NULL, 'I'),
(002, "Groceries", "For grocery expenses", 'E'),
(003, "Bills", "For bill expenses", 'E');
"""
insert_trans = """
insert into trans values
(001, "2022-02-16", 23.20, "allowance", 'I', NULL, 001),
(002, "2022-02-16", 256.99, "February groceries", 'E', NULL, 002),
(003, "2022-02-16", 30.00, "Joe paid me back", 'I', NULL, 001),
(004, "2022-02-16", 600.00, "February Rent", 'E', NULL, 003);
"""

cur.execute(category_table)
cur.execute(recurring_table)
cur.execute(trans_table)
cur.execute(insert_cat)
cur.execute(insert_trans)

cur.execute('select * from trans;')
result = cur.fetchall()
print(result)

conn.close()