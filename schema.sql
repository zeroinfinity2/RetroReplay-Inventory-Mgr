DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Consoles;
DROP TABLE IF EXISTS ConsoleTypes;
DROP TABLE IF EXISTS MerchTypes;


CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    AcquiredDate VARCHAR(8) NOT NULL,
    ProductCode VARCHAR(255),
    ProductSold int NOT NULL DEFAULT 0
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

CREATE TABLE ConsoleTypes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeName VARCHAR(255) NOT NULL,
    ImgFile VARCHAR(255) NOT NULL
);

CREATE TABLE MerchTypes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeName VARCHAR(255) NOT NULL
);

INSERT INTO ConsoleTypes (TypeName, ImgFile)
VALUES ('PSX', 'PSX.png'), ('SAT', 'SAT.png'), ('GEN', 'GEN.png'), ('N64', 'N64.png'), ('SFC', 'SFC.png'), ('NES', 'NES.png'), ('GB', 'GB.png');