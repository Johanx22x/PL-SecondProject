from app import Program
from app.sqlite import SQLite
from app.prolog import Prolog


db = SQLite("./testdb.sqlite")
prolog = Prolog()

if __name__ == "__main__":
    try:
        Program().run()
    except KeyboardInterrupt:
        prolog.close()
        db.close()
