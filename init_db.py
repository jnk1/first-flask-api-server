import sqlite3

dbname = 'test.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS recipes (
    id integer PRIMARY KEY AUTOINCREMENT,
    -- name of recipe
    title text,
    -- time required to cook/bake the recipe
    making_time text,
    -- number of people the recipe will feed
    serves text,
    -- food items necessary to prepare the recipe
    ingredients text,
    -- price of recipe
    cost integer NOT NULL,
    created_at timestampe NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    updated_at timestampe NOT NULL DEFAULT (DATETIME('now', 'localtime'))
    )'''
)

cur.execute(
    '''CREATE TRIGGER my_trigger AFTER UPDATE ON recipes
        BEGIN
            UPDATE recipes SET updated_at = DATETIME('now', 'localtime') WHERE rowid == NEW.rowid;
        END;
''')

cur.execute('''INSERT INTO recipes (id, title, making_time, serves, ingredients,
    COST, created_at, updated_at)
    VALUES (1, 'チキンカレー', '45分', '4人', '玉ねぎ,肉,スパイス', 1000, '2016-01-10 12:10:12', '2016-01-10 12:10:12');
''')

cur.execute('''INSERT INTO recipes (id, title, making_time, serves, ingredients,
    COST, created_at, updated_at)
    VALUES (2, 'オムライス', '30分', '2人', '玉ねぎ,卵,スパイス,醤油', 700, '2016-01-11 13:10:12', '2016-01-11 13:10:12');

''')
conn.commit()

cur.close()
conn.close()
