import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '../database/pedidos.db')

def init_db():
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        schema_sql = f.read()

    conn = sqlite3.connect(db_path)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Base de datos creada correctamente.")

if __name__ == "__main__":
    init_db()
