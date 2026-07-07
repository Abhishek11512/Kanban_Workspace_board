import sqlite3

con = sqlite3.connect('tasks.db')
cr = con.cursor()

cr.execute('''CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(100),
status VARCHAR(30))''')

con.commit()
con.close()
print("DATABASE CREATED SUCCESSFULLY!")