import sqlite3
DATABASE = 'database.db'

def create_tables():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS foods (id, name, protein, fat, carbohydrate)")
    con.execute("CREATE TABLE IF NOT EXISTS dishes (id, name)")
    con.execute("CREATE TABLE IF NOT EXISTS foods_dishes (id, id_dish, id_food, quantity)")
    con.close()
