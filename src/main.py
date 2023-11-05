from app import Program
from app import Prolog
from app import SQLite


p = Program()
db = SQLite("./testdb.sqlite")
prolog = Prolog()

if __name__ == "__main__":
    try:
        p.run()
    except KeyboardInterrupt:
        prolog.close()
        db.close()
