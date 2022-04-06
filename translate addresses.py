from transliterate import translit
from const_for_main import CONNECTION
import sqlite3

con = sqlite3.connect(CONNECTION)
cur = con.cursor()
# addresses = cur.execute("SELECT id, address FROM addresses").fetchall()
# for add in addresses:
#     text = translit(add[1], reversed=True)
#     cur.execute("UPDATE addresses SET eng_address=? WHERE id=?", (text, add[0]))
#     print(add[0], text)

regions = cur.execute("SELECT id, eng_address FROM addresses").fetchall()
for add in regions:
    text = cur.execute("SELECT eng_address FROM addresses WHERE id=?", (add[0], )).fetchone()[0]
    print(text)
    text = text.replace('Moskva', 'Moscow').replace('Sankt-Peterburg', 'Saint Petersburg').replace('etazh', 'floor')
    cur.execute("UPDATE addresses SET eng_address=? WHERE id=?", (text, add[0]))
    print(add[0], text)
con.commit()
con.close()