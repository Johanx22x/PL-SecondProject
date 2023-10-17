from sqlite3 import connect

db = connect("sqlite://../../testdb.sqlite", check_same_thread=False)
db.execute("PRAGMA foreign_keys = ON;")
