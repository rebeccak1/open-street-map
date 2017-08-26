
print "Number of nodes:"
cur.execute('SELECT COUNT(*) FROM nodes').fetchone()[0]

print "Number of ways:"
cur.execute('SELECT COUNT(*) FROM ways').fetchone()[0]

print "Number of unique users:"
cur.execute('SELECT COUNT(DISTINCT(e.uid)) \
            FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e').fetchone()[0]

print "Top 10 contributing users:"
users = []
for row in cur.execute('SELECT e.user, COUNT(*) as num \
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
            GROUP BY e.user \
            ORDER BY num DESC \
            LIMIT 10'):
    users.append(row)
print users

print "Number of users contributing once:"
cur.execute('SELECT COUNT(*) FROM \
                (SELECT e.user, COUNT(*) as num \
                 FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                 GROUP BY e.user \
                 HAVING num=1) u').fetchone()[0]

print "Top 10 amenities:"
amenities = []
for row in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
            WHERE key="amenity" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
    amenities.append(row)
print amenities

print "Top 5 places of worship:"
religions = []
for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="religion" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC \
            LIMIT 5;'):
    religions.append(row)
print religions

print "Top 5 cuisines"
cuisines = []
for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="cuisine" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC \
            LIMIT 5'):
    cuisines.append(row)
print cuisines

print "Top 10 restaurants:"
restaurants = []
for row in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="restaurant") i \
                ON nodes_tags.id=i.id \
            WHERE key="name"\
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
    restaurants.append(row)
print restaurants