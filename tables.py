import sqlite3

conn = sqlite3.connect("data/medicine.db")
cursor = conn.cursor()

cursor.execute("""
SELECT generic_name, interaction
FROM generic
WHERE interaction IS NOT NULL
LIMIT 5
""")

rows = cursor.fetchall()

for row in rows:
    print("=" * 60)
    print("Medicine:", row[0])
    print("Interaction:")
    print(row[1])

conn.close()