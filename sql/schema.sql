CREATE TABLE Employee (
    id_employee VARCHAR(10) NOT NULL PRIMARY KEY,
    empl_surname VARCHAR(50) NOT NULL,
    empl_name VARCHAR(50) NOT NULL,
    empl_patronymic VARCHAR(50) NULL,
    empl_role VARCHAR(10) NOT NULL,
    salary DECIMAL(13,4) NOT NULL,
    date_of_birth DATE NOT NULL,
    date_of_start DATE NOT NULL,
    phone_number VARCHAR(13) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    zip_code VARCHAR(9) NOT NULL
);

CREATE TABLE Category (
       category_number SERIAL NOT NULL PRIMARY KEY,
       category_name VARCHAR(50) NOT NULL
);

CREATE TABLE Product (
       id_product SERIAL NOT NULL PRIMARY KEY,
       category_number INTEGER NOT NULL REFERENCES Category(category_number)
           ON UPDATE CASCADE
           ON DELETE NO ACTION,
       product_name VARCHAR(50) NOT NULL,
       characteristics VARCHAR(100) NOT NULL
);

CREATE TABLE Customer_Card (
    card_number VARCHAR(13) NOT NULL PRIMARY KEY,
    cust_surname VARCHAR(50) NOT NULL,
    cust_name VARCHAR(50) NOT NULL,
    cust_patronymic VARCHAR(50) NULL,
    phone_number VARCHAR(13) NOT NULL,
    city VARCHAR(50) NULL,
    street VARCHAR(50) NULL,
    zip_code VARCHAR(9) NULL,
    percent INTEGER NOT NULL
);

CREATE TABLE "Check" (
    check_number VARCHAR(10) NOT NULL PRIMARY KEY,
    id_employee VARCHAR(10) NOT NULL REFERENCES Employee(id_employee)
                ON UPDATE CASCADE
                ON DELETE NO ACTION,
    card_number VARCHAR(13) NULL REFERENCES Customer_Card(card_number)
                ON UPDATE CASCADE
                ON DELETE NO ACTION,
    print_date TIMESTAMP NOT NULL,
    sum_total DECIMAL(13,4) NOT NULL,
    vat DECIMAL(13,4) NOT NULL
);

CREATE TABLE Store_Product (
    UPC VARCHAR(12) NOT NULL PRIMARY KEY,
    UPC_prom VARCHAR(12) NULL REFERENCES Store_Product(UPC)
            ON UPDATE CASCADE
            ON DELETE SET NULL,
    id_product INTEGER NOT NULL REFERENCES Product(id_product)
                ON UPDATE CASCADE
                ON DELETE NO ACTION,
    selling_price DECIMAL(13,4) NOT NULL,
    products_number INTEGER NOT NULL,
    promotional_product BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Sale (
    UPC VARCHAR(12) NOT NULL REFERENCES Store_Product(UPC)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    check_number VARCHAR(10) NOT NULL REFERENCES "Check"(check_number)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
    product_number INTEGER NOT NULL,
    selling_price DECIMAL(13,4) NOT NULL,
    PRIMARY KEY (UPC, check_number)
)