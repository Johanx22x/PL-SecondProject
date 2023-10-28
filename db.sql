PRAGMA encoding = "UTF-8";
PRAGMA foreign_keys = ON;  -- Enable foreign key support

-- Foods table with ON DELETE CASCADE
CREATE TABLE Foods (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type        INTEGER DEFAULT 0,
    subtype     INTEGER DEFAULT 0,
    name        TEXT    DEFAULT "Unnamed food :^)",
    calories    FLOAT   DEFAULT 0.0,
    price       FLOAT   DEFAULT 0.0
);

-- Tables table with ON DELETE CASCADE
CREATE TABLE Tables (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    DEFAULT "Unnamed table :^)",
    people      INTEGER DEFAULT 0
);

-- Bills table with ON DELETE CASCADE
CREATE TABLE Bills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    total       FLOAT   DEFAULT 0.0,
    date_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    type        INTEGER DEFAULT 1,
    table_id    INTEGER,
    FOREIGN KEY (table_id) REFERENCES Tables(id) ON DELETE CASCADE
);

-- Orders table with ON DELETE CASCADE
CREATE TABLE Orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id     INTEGER,
    is_healthy  INTEGER DEFAULT 0,
    FOREIGN KEY (bill_id) REFERENCES Bills(id) ON DELETE CASCADE
);

-- Dishes table with ON DELETE CASCADE
CREATE TABLE Dishes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    DEFAULT "Unnamed dish :^)",
    type        INTEGER DEFAULT 0,
    is_predef   INTEGER DEFAULT 1
);

-- Dishes_Foods table with ON DELETE CASCADE
CREATE TABLE Dishes_Foods (
    dish_id     INTEGER,
    food_id     INTEGER,
    FOREIGN KEY (dish_id) REFERENCES Dishes(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES Foods(id) ON DELETE CASCADE
);

-- Dishes_Orders table with ON DELETE CASCADE
CREATE TABLE Dishes_Orders (
    dish_id INTEGER,
    order_id INTEGER,
    FOREIGN KEY (dish_id) REFERENCES Dishes(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE
);

-- Statistics table without ON DELETE CASCADE
CREATE TABLE Statistics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time       DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_sales     FLOAT   DEFAULT 0.0,
    inventory_items INTEGER DEFAULT 0,
    menu_items      INTEGER DEFAULT 0,
    total_orders    INTEGER DEFAULT 0
);

-- Trigger to update the Statistics table 
CREATE TRIGGER update_statistics_bills
AFTER INSERT ON Bills
BEGIN
    UPDATE Statistics SET total_sales = total_sales + new.total;
    UPDATE Statistics SET total_orders = total_orders + 1;
END;

CREATE TRIGGER update_statistics_foods
AFTER INSERT ON Foods 
BEGIN
    UPDATE Statistics SET inventory_items = inventory_items + 1;
END;

CREATE TRIGGER update_statistics_foods_delete
AFTER DELETE ON Foods 
BEGIN
    UPDATE Statistics SET inventory_items = inventory_items - 1;
END;

CREATE TRIGGER update_statistics_dishes
AFTER INSERT ON Dishes 
BEGIN
    UPDATE Statistics SET menu_items = menu_items + 1;
END;

CREATE TRIGGER update_statistics_dishes_delete
AFTER DELETE ON Dishes 
BEGIN
    UPDATE Statistics SET menu_items = menu_items - 1;
END;

-- Create a trigger that detects when a food that is part of a dish is deleted, and deletes the dish 
CREATE TRIGGER on_delete_food_delete_dish
BEFORE DELETE ON Foods
FOR EACH ROW
BEGIN
    DELETE FROM Dishes WHERE id IN (SELECT dish_id FROM Dishes_Foods WHERE food_id = OLD.id);
END;

-- Create first row in the Statistics table 
INSERT INTO Statistics (total_sales, inventory_items, menu_items, total_orders) VALUES (0.0, 0, 0, 0);

-- Inserting various food items into the Food table
-- Drink category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 1, 'Soda', 150.0, 1.99); -- Drink - Soda
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 2, 'Orange Juice', 120.0, 2.49); -- Drink - Natural
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 3, 'Mineral Water', 0.0, 1.29); -- Drink - Water Based
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 4, 'Milk', 80.0, 1.79); -- Drink - Milk Based
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 5, 'Coffee', 5.0, 1.49); -- Drink - Hot
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 6, 'Iced Tea', 20.0, 1.99); -- Drink - Cold

-- Protein category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 7, 'Beef Steak', 450.0, 15.99); -- Protein - Red Meat
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 7, 'Pork Chop', 400.0, 13.99); -- Protein - Red Meat
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 8, 'Grilled Chicken Breast', 350.0, 11.99); -- Protein - Chicken
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 8, 'BBQ Chicken', 400.0, 12.99); -- Protein - Chicken
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 9, 'Grilled Salmon', 400.0, 16.99); -- Protein - Fish
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 9, 'Salmon', 400.0, 15.99); -- Protein - Fish
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 10, 'Shrimp', 200.0, 14.99); -- Protein - Seafood
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 10, 'Lobster', 300.0, 19.99); -- Protein - Seafood
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 10, 'Crab', 200.0, 17.99); -- Protein - Seafood

-- Side Dish category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 12, 'French Fries', 365.0, 3.99); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 11, 'Steamed Vegetables', 150.0, 4.49); -- Side Dish - Vegetables
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 12, 'Mashed Potatoes', 250.0, 3.79); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 12, 'Baked Potato', 200.0, 2.99); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 11, 'Green Salad', 100.0, 5.99); -- Side Dish - Vegetables
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 11, 'Caesar Salad', 200.0, 6.49); -- Side Dish - Vegetables

-- Dessert category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 13, 'Chocolate Cake', 500.0, 7.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 15, 'Apple Pie', 300.0, 6.49); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 13, 'Ice Cream', 250.0, 4.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 11, 'Frozen Yogurt', 200.0, 3.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 14, 'Tofu', 200.0, 5.49); -- Protein - Vegetarian

-- Create predefined dishes
INSERT INTO Dishes (name) VALUES ('Steak and Fries');
INSERT INTO Dishes (name) VALUES ('Juice and Salad');
INSERT INTO Dishes (name) VALUES ('Salmon and Potatoes');
INSERT INTO Dishes (name) VALUES ('Chicken and Salad');
INSERT INTO Dishes (name) VALUES ('Shrimp and Salad');
INSERT INTO Dishes (name) VALUES ('Lobster and Vegetables');

-- Inserting food items into the Dishes_Foods table
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (1, 9);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (1, 14);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (2, 2);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (2, 21);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (3, 11);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (3, 14);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (4, 10);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (4, 13);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (5, 12);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (5, 13);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (6, 12);
INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (6, 14);

INSERT INTO Tables (name, people) VALUES ('Table 1', 4);
INSERT INTO Tables (name, people) VALUES ('Table 2', 5);
INSERT INTO Tables (name, people) VALUES ('Table 3', 3);
INSERT INTO Tables (name, people) VALUES ('Table 4', 2);

-- Inserting bills into the Bills table 
INSERT INTO Bills (total, date_time, type, table_id) VALUES (32.5, '2017-01-01 12:53:00', 1, 1);
INSERT INTO Bills (total, date_time, type, table_id) VALUES (12.1, '2017-01-01 13:04:00', 2, 2);
INSERT INTO Bills (total, date_time, type, table_id) VALUES (18.0, '2017-01-04 15:23:00', 1, 3);

INSERT INTO Orders (bill_id) VALUES (1);
INSERT INTO Orders (bill_id) VALUES (1);
INSERT INTO Orders (bill_id) VALUES (1);
INSERT INTO Orders (bill_id) VALUES (2);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);
INSERT INTO Orders (bill_id) VALUES (3);

INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (1, 1);
INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (2, 2);
INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (2, 3);
INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (4, 4);
INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (5, 5);
