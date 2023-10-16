PRAGMA foreign_keys = on;
PRAGMA encoding = "UTF-8";

CREATE TABLE Foods (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type        INTEGER DEFAULT 0,
    subtype     INTEGER DEFAULT 0,
    name        TEXT    DEFAULT "Unnamed food :^)",
    calories    FLOAT   DEFAULT 0.0,
    price       FLOAT   DEFAULT 0.0
);

-- Inserting various food items into the Food table
-- Drink category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 1, 'Soda', 150.0, 1.99); -- Drink - Soda
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 3, 'Orange Juice', 120.0, 2.49); -- Drink - Natural
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 3, 'Mineral Water', 0.0, 1.29); -- Drink - Water Based
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 4, 'Milk', 80.0, 1.79); -- Drink - Milk Based
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 5, 'Coffee', 5.0, 1.49); -- Drink - Hot
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (1, 6, 'Iced Tea', 20.0, 1.99); -- Drink - Cold

-- Protein category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 9, 'Beef Steak', 450.0, 15.99); -- Protein - Red Meat
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 9, 'Pork Chop', 400.0, 13.99); -- Protein - Red Meat
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 10, 'Grilled Chicken Breast', 350.0, 11.99); -- Protein - Chicken
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 10, 'BBQ Chicken', 400.0, 12.99); -- Protein - Chicken
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 11, 'Grilled Salmon', 400.0, 16.99); -- Protein - Fish
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 11, 'Salmon', 400.0, 15.99); -- Protein - Fish
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 12, 'Shrimp', 200.0, 14.99); -- Protein - Seafood
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 12, 'Lobster', 300.0, 19.99); -- Protein - Seafood
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (2, 12, 'Crab', 200.0, 17.99); -- Protein - Seafood

-- Side Dish category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 14, 'French Fries', 365.0, 3.99); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 13, 'Steamed Vegetables', 150.0, 4.49); -- Side Dish - Vegetables
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 14, 'Mashed Potatoes', 250.0, 3.79); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 14, 'Baked Potato', 200.0, 2.99); -- Side Dish - Carbs
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 13, 'Green Salad', 100.0, 5.99); -- Side Dish - Vegetables
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (3, 13, 'Caesar Salad', 200.0, 6.49); -- Side Dish - Vegetables

-- Dessert category
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 16, 'Chocolate Cake', 500.0, 7.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 17, 'Apple Pie', 300.0, 6.49); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 15, 'Ice Cream', 250.0, 4.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 15, 'Frozen Yogurt', 200.0, 3.99); -- Dessert
INSERT INTO Foods (type, subtype, name, calories, price) VALUES (4, 15, 'Tofu', 200.0, 5.49); -- Protein - Vegetarian


-- Predefined dishes tables
CREATE TABLE Dishes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    DEFAULT "Unnamed dish :^)",
    type        INTEGER DEFAULT 0
);

CREATE TABLE Dishes_Foods (
    dish_id     INTEGER,
    food_id     INTEGER,
    FOREIGN KEY (dish_id) REFERENCES Dishes(id),
    FOREIGN KEY (food_id) REFERENCES Foods(id)
);

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


-- Billing system and statistics tables
CREATE TABLE Tables (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    DEFAULT "Unnamed table :^)",
    people      INTEGER DEFAULT 0
);

CREATE TABLE Bills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    total       FLOAT   DEFAULT 0.0,
    date_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    type        INTEGER DEFAULT 0,
    table_id    INTEGER,
    FOREIGN KEY (table_id) REFERENCES Tables(id)
);

CREATE TABLE Orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id     INTEGER,
    bill_id     INTEGER,
    FOREIGN KEY (food_id) REFERENCES Foods(id),
    FOREIGN KEY (bill_id) REFERENCES Bills(id)
);
