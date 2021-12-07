from transliterate import translit
from const_for_main import CONNECTION
import sqlite3

# con = sqlite3.connect(CONNECTION)
# cur = con.cursor()
# addresses = cur.execute("SELECT id, address FROM addresses").fetchall()
# for add in addresses:
#     text = translit(add[1], reversed=True)
#     cur.execute("UPDATE addresses SET eng_address=? WHERE id=?", (text, add[0]))
#     print(add[0], text)

# regions = cur.execute("SELECT id, region FROM id_regions").fetchall()
# for add in regions:
#     text = str(translit(add[1], reversed=True))
#     text = text.replace('Respublika', 'Republic').replace('kraj', 'krai').replace("oblast'", 'oblast')
#     cur.execute("UPDATE id_regions SET eng_region=? WHERE id=?", (text, add[0]))
#     print(add[0], text)
# con.commit()
# con.close()
reg = []
for i in range(86):
    reg.append(f"{i + 1} {input()}")

print(reg)