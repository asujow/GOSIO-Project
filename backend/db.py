# backend/db.py
import sqlite3
def get_conn():
    c=sqlite3.connect("./data/knowledge.db")
    c.row_factory=sqlite3.Row
    return c
def fetch_components():
    conn=get_conn()
    cur=conn.execute("SELECT * FROM Componente")
    rows=[dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
def fetch_keywords_for_component(cid):
    conn=get_conn()
    cur=conn.execute("SELECT keyword FROM Keyword WHERE componente_id=?", (cid,))
    res=[r["keyword"] for r in cur.fetchall()]
    conn.close()
    return res
