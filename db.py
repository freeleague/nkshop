import sqlite3
import asyncio

async def users(id):
    with sqlite3.connect("work.db") as c:
        check = c.execute("SELECT id FROM users WHERE id = ?", (id,)).fetchone()
        if check is None:
            c.execute("INSERT INTO users VALUES(?)", (id,))
        else:
            pass

async def all_user():
    with sqlite3.connect('work.db') as c:
        all = c.execute("SELECT * FROM users").fetchall()
        return len(all)

async def add_tovar(tovars):
    tovar = tovars.split(':')
    print(tovar)
    if len(tovar) == 4:
        name = tovar[0]
        gramm = tovar[1]
        price = tovar[2]
        tip = tovar[3]
        with sqlite3.connect('work.db') as c:
            c.execute('INSERT INTO drugs VALUES(?,?,?,?)',(name,gramm,price,tip))
            return True
    else:
        return False

async def delete_tovar(tovars):
    tovar = tovars.split(':')
    if len(tovar) == 2:
        name = tovar[0]
        gramm = tovar[1]
        with sqlite3.connect('work.db') as c:
            c.execute('DELETE FROM drugs WHERE name=? AND gramm = ? ',(name,gramm,))
            return True
    else:
        return False