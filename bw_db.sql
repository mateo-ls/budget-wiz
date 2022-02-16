create schema budgetwiz;

use budgetwiz;

/* ----- CREATE TABLES ----- */

/* stores a single transaction*/
create table transaction(
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

/* stores instructions for a recurring transaction, which repeats monthly */
create table recurring(
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

/* stores category information */
create table category(
    CategoryID INT NOT NULL,
    CategoryName VARCHAR(255) NOT NULL,
    Description VARCHAR(255),
    CONSTRAINT catPK PRIMARY KEY (CategoryID)
);

/* ----- INSERT SAMPLE VALUES ----- */

insert into category values
(001, "General", NULL),
(002, "Groceries", "For grocery expenses"),
(003, "Bills", "For bill expenses");

insert into transaction values
(001, "2022-02-16", 23.20, "allowance", 'I', NULL, 001),
(002, "2022-02-16", 256.99, "February groceries", 'E', NULL, 002),
(003, "2022-02-16", 30.00, "Joe paid me back", 'I', NULL, 001),
(004, "2022-02-16", 600.00, "February Rent", 'E', NULL, 003);