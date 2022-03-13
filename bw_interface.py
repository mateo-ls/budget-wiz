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
            CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            CategoryName VARCHAR(255) NOT NULL,
            Description VARCHAR(255),
            IncomeOrExpense CHAR NOT NULL
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

insert_cat = """
insert into category values
(001, "General", NULL, 'I'),
(002, "Groceries", "For grocery expenses", 'E'),
(003, "Bills", "For bill expenses", 'E');
"""

cur.execute(category_table)
cur.execute(recurring_table)
cur.execute(trans_table)
#cur.execute(insert_cat)

transaction = """
        INSERT into trans (InputDate, Amount, Description, IncomeOrExpense, RecurrenceID, CategoryID)
        values (?, ?, ?, ?, ?, ?);
        """

values = ("2022-01-05", 200, "hello", 'E', 1, 1)
cur.execute(transaction, values)
conn.commit()

cur.execute('select * from trans;')
result = cur.fetchall()
print(result)

conn.close()