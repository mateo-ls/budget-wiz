create table category(
    CategoryID INTEGER PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(255) NOT NULL,
    Description VARCHAR(255),
    IncomeOrExpense CHAR NOT NULL,
    UNIQUE(CategoryName, IncomeOrExpense)
);

create table recurring(
    RecurrenceID INTEGER PRIMARY KEY AUTO_INCREMENT,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Amount DECIMAL(38,2) NOT NULL,
    Description VARCHAR(45),
    IncomeOrExpense CHAR NOT NULL, /* 'I' = Income, 'E' = Expense */
    CategoryID INT NOT NULL,
    CONSTRAINT catFK2 FOREIGN KEY (CategoryID) REFERENCES category(CategoryID)
);

create table trans(
    TransactionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    InputDate DATE NOT NULL,
    Amount DECIMAL(38,2) NOT NULL,
    Description VARCHAR(45),
    IncomeOrExpense CHAR, /* 'I' = Income, 'E' = Expense */
    RecurrenceID INT,
    CategoryID INT NOT NULL,
    CONSTRAINT recFK FOREIGN KEY (CategoryID) REFERENCES category(CategoryID),
    CONSTRAINT catFK1 FOREIGN KEY (RecurrenceID) REFERENCES recurring(RecurrenceID)
);

insert into category (CategoryName, Description, IncomeOrExpense) values
("General", NULL, 'I'),
("Groceries", "For grocery expenses", 'E'),
("Bills", "For bill expenses", 'E');

insert into trans values
(001, "2022-02-16", 23.20, "Allowance", 'I', NULL, 001),
(002, "2022-02-18", 256.99, "February groceries", 'E', NULL, 002),
(003, "2022-02-25", 30.00, "Joe paid me back", 'I', NULL, 001),
(004, "2022-02-28", 600.00, "February Rent", 'E', NULL, 003),
(005, "2022-03-03", 3000.00, "Robbed local bank", 'I', NULL, 001),
(006, "2022-04-24", 3500.00, "Feds got me", 'E', NULL, 003),
(007, "2022-04-25", 2000.00, "Child support", 'E', NULL, 003);

select sum(Amount) from trans
where IncomeOrExpense='I' and
month(InputDate)=02 and
year(InputDate)=2022;

select sum(Amount) from trans
where IncomeOrExpense='E' and
month(InputDate)=02 and
year(InputDate)=2022;

