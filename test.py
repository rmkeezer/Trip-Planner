import sqlite3
db = sqlite3.connect('test.db')
with open('team4-schema.sql', 'r') as f:
    db.cursor().executescript(f.read())
db.commit()