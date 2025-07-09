import sqlite3
import os

DB_PATH = "facturi.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS facturi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nr_factura TEXT,
                data TEXT,
                client TEXT,
                platforma TEXT,
                cod_rezervare TEXT,
                fisier TEXT
            )
        """)
        conn.execute("""
                    CREATE TABLE IF NOT EXISTS config (
                        cheie TEXT PRIMARY KEY,
                        valoare INTEGER
                    )
                """)
        
        cur = conn.execute("SELECT COUNT(*) FROM config WHERE cheie = 'nr_factura_curent'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO config (cheie, valoare) VALUES ('nr_factura_curent', 1)")

def exista_factura(serie_si_nr):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM facturi WHERE nr_factura = ?", (serie_si_nr,))
        return cur.fetchone()[0] > 0
    
def get_nr_factura_curent():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT valoare FROM config WHERE cheie = 'nr_factura_curent'").fetchone()
        return result[0] if result else 1

def increment_nr_factura():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE config SET valoare = valoare + 1 WHERE cheie = 'nr_factura_curent'")

def get_urmatorul_numar_factura():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT MAX(nr_factura) FROM facturi").fetchone()
        return (result[0] or 0) + 1

def salveaza_factura(nr, data, client, platforma, cod, fisier):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO facturi (nr_factura, data, client, platforma, cod_rezervare, fisier)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nr, data, client, platforma, cod, fisier))

def sterge_factura(nr_factura):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM facturi WHERE nr_factura = ?", (nr_factura,))
        # conn.execute("DELETE FROM facturi")

def incarca_facturi():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT nr_factura, data, client, platforma, cod_rezervare, fisier 
            FROM facturi 
            ORDER BY nr_factura DESC
        """).fetchall()