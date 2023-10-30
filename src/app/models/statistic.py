from typing import Self, List, Any, Dict, Optional
from datetime import datetime
from app.models.model_protocol import Modelable
from app.sqlite import SQLite

class Statistic(Modelable):
    _db = SQLite()

    def __init__(self: Self) -> None:
        super().__init__()
        self.id = 0
        self.date_time = datetime.now()
        self.total_sales = 0.0
        self.inventory_items = 0 
        self.menu_items = 0 
        self.total_orders = 0

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_date_time(self: Self, date_time: datetime) -> Self:
        self.date_time = date_time
        return self 

    def with_total_sales(self: Self, total_sales: float) -> Self:
        self.total_sales = total_sales
        return self

    def with_inventory_items(self: Self, inventory_items: int) -> Self:
        self.inventory_items = inventory_items
        return self

    def with_menu_items(self: Self, menu_items: int) -> Self:
        self.menu_items = menu_items
        return self 

    def with_total_orders(self: Self, total_orders: int) -> Self:
        self.total_orders = total_orders
        return self 

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, date_time, total_sales, inventory_items, menu_items, total_orders = row
        return cls().with_id(id).with_date_time(date_time).with_total_sales(total_sales).with_inventory_items(inventory_items).with_menu_items(menu_items).with_total_orders(total_orders)

    @classmethod 
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod 
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Statistics")
        return Statistic.from_rows(cur.fetchall())

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Statistics WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return cls.from_row(row)

    @classmethod
    def latest(cls) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Statistics ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        if row is None:
            return None
        return cls.from_row(row)

    @classmethod
    def sales_and_income_by_date_range(cls, start_date: datetime, end_date: datetime) -> List[Self]:
        cur = cls._db.execute("SELECT DATE(b.date_time) AS order_date, SUM(orders_per_bill.total_orders) AS total_sales, SUM(b.total) AS total_income FROM Bills b JOIN ( SELECT bill_id, COUNT(*) AS total_orders FROM Orders GROUP BY bill_id) AS orders_per_bill ON b.id = orders_per_bill.bill_id WHERE DATE(b.date_time) BETWEEN ? AND ? GROUP BY order_date;", [start_date, end_date])
        return cur.fetchall()

    @classmethod
    def top_menu_items(cls) -> List[Self]:
        cur = cls._db.execute("SELECT d.name AS name, COUNT(do.dish_id) AS amount FROM Dishes d JOIN Dishes_Orders do ON do.dish_id = d.id JOIN Orders o ON o.id = do.order_id WHERE o.is_healthy = 0 AND d.is_predef = 1 GROUP BY d.name ORDER BY amount DESC LIMIT 3;")
        return cur.fetchall()

    @classmethod
    def top_inventory_items(cls) -> List[Self]:
        cur = cls._db.execute("SELECT f.name AS name, COUNT(fo.food_id) AS amount FROM Foods f JOIN Dishes_Foods fo ON fo.food_id = f.id JOIN Dishes d ON d.id = fo.dish_id JOIN Dishes_Orders do ON do.dish_id = d.id JOIN Orders o ON o.id = do.order_id WHERE o.is_healthy = 1 AND d.is_predef = 0 GROUP BY f.name ORDER BY amount DESC LIMIT 3;")
        return cur.fetchall()

    def to_dict(self: Self) -> Dict:
        return {"id": self.id, "date_time": self.date_time, "total_sales": self.total_sales, "inventory_items": self.inventory_items, "menu_items": self.menu_items, "total_orders": self.total_orders}
