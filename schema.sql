DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Consoles;
DROP TABLE IF EXISTS GeneralGoods;
DROP TABLE IF EXISTS ConsoleTypes;


CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    ProductIdentifier VARCHAR(5) NOT NULL UNIQUE,
    InDate INTEGER NOT NULL UNIQUE,
    ProductType INTEGER NOT NULL,
    ProductSold BOOLEAN NOT NULL DEFAULT 0,
    ProductCost DECIMAL(8, 2) NOT NULL,
    ProductPrice DECIMAL(8, 2),
    ProductCode VARCHAR(255)
);

CREATE TABLE Consoles (
    ConsoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    ConsoleMods VARCHAR(255),
    ConsoleModel VARCHAR(3) NOT NULL,
    ConsoleBoard VARCHAR(255) NOT NULL,
    ProductCode VARCHAR(255),
    ConsoleCode VARCHAR(255),
    FOREIGN KEY (ProductCode) REFERENCES 
    Products(ProductCode),
    FOREIGN KEY (ConsoleCode) REFERENCES
    Products(ProductIdentifier)
);

CREATE TABLE GeneralGoods (
    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductCode VARCHAR(255),
    ItemStock INTEGER NOT NULL DEFAULT 0,
    ImgFile VARCHAR(255) NOT NULL,
    FOREIGN KEY (ProductCode) REFERENCES 
    Products(ProductCode)
);

CREATE TABLE ConsoleTypes (
    ConsoleCode VARCHAR(10) PRIMARY KEY,
    ConsoleName VARCHAR(255) NOT NULL,
    ImgFile VARCHAR(255) NOT NULL
);

INSERT INTO ConsoleTypes (ConsoleCode, ConsoleName, ImgFile)
VALUES ('PSX', 'Playstation', 'PSX.png'), ('SAT', 'Sega Saturn', 'SAT.png'), ('GEN', 'Sega Genesis', 
'GEN.png'), ('N64', 'Nintendo 64', 'N64.png'), ('SFC', 'Super Nintendo', 'SFC.png'), ('NES', 'NES', 'NES.png'), ('GB', 'Game Boy', 'GB.png');