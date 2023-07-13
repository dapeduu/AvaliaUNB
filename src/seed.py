from db import Database
import sys

db = Database()
# Cria as tabelas
with open(sys.path[0] + "/sql/database.sql", "r") as file:
    db.db.execute(file.read())
    db.db.commit()

# Popula as tabelas
with open(sys.path[0] + "/sql/populate_database.sql", "r") as file:
    db.db.execute(file.read())
    db.db.commit()
