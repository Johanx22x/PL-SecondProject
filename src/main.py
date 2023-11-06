from app import Program
from app import Prolog
from app import SQLite


p = Program()
db = SQLite("./testdb.sqlite")
prolog = Prolog()

food_elements = db.execute("SELECT * FROM Foods")
for food in food_elements:
    prolog.query(
        # Assert the food
        f"assertz(food({food[1]}, {food[2]}, '{food[3]}', {food[4]}, {food[5]}))."
    )
prolog.query("consult('./src/main.pl')")

if __name__ == "__main__":
    try:
        p.run()
    except KeyboardInterrupt:
        prolog.close()
        db.close()
