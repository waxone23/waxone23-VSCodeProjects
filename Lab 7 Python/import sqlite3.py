import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM students")

print(cursor.fetchone())
conn.close()
