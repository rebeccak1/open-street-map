import csv
import sqlite3

conn = sqlite3.connect('tampa2.db')
conn.text_factory = str
cur = conn.cursor()

cur.execute('CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT);')
with open('nodes.csv','rb') as fname:
    dr = csv.DictReader(fname)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) \
             for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

cur.execute("CREATE TABLE nodes_tags (id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes(id));")
with open('nodes_tags.csv','rb') as fname:
    dr = csv.DictReader(fname) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

cur.execute("CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT);")
with open('ways.csv','rb') as fname:
    dr = csv.DictReader(fname) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

cur.execute("CREATE TABLE ways_nodes (id INTEGER NOT NULL, node_id INTEGER NOT NULL, position INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES ways(id), FOREIGN KEY (node_id) REFERENCES nodes(id));")
with open('ways_nodes.csv','rb') as fname:
    dr = csv.DictReader(fname) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
conn.commit()

cur.execute("CREATE TABLE ways_tags (id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, type TEXT, FOREIGN KEY (id) REFERENCES ways(id));")
with open('ways_tags.csv','rb') as fname:
    dr = csv.DictReader(fname) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()