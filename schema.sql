DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Consoles;

CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    AcquiredDate VARCHAR(8) NOT NULL,
    ProductCode VARCHAR(255)
);

CREATE TABLE Consoles (
    ConsoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    ConsoleMods VARCHAR(255),
    ConsoleModel VARCHAR(3) NOT NULL,
    ConsoleBoard VARCHAR(255) NOT NULL,
    ProductCode VARCHAR(255),
    FOREIGN KEY (ProductCode) REFERENCES 
    Products(ProductCode)
);