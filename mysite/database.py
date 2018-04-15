import sqlite3 as lite


# Создание бд
def createDB():
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS usersENG
             (id integer NOT NULL  primary key ,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS usersTWI
             (id integer NOT NULL  primary key ,
             name text,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS usersKINONEG
             (id integer NOT NULL  primary key ,
             name text,
             film text,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS usersKINOPOS
             (id integer NOT NULL  primary key ,
             name text,
             film text,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS usersKINONET
             (id integer NOT NULL  primary key ,
             name text,
             film text,
             review text,
             mark int)""")
    db.commit()
    db.close()


# Новая запись: для кинопоиска Входные данные ('человек','plohie parni','ochen krutoi film',1,'20.10.2012')
# Для твиттера и англа 4 на вход без фильма
def new_rec(in_data, table):
    db = lite.connect('analitics.db')
    c = db.cursor()
    if table in ["usersTWI"]:
        c.execute("INSERT INTO '" + table + "' (name, review, mark) VALUES (?,?,?)", in_data)
    elif table in ["usersENG"]:
        c.execute("INSERT INTO '" + table + "' (review, mark) VALUES (?,?)", in_data)
    else:
        c.execute("INSERT INTO '" + table + "' (name, film, review, mark) VALUES (?,?,?,?)", in_data)

    db.commit()
    db.close()


# Средняя по имени пользователя
def avgsumbyName(tname, changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("SELECT avg(mark) FROM '" + changetable + "' WHERE name=? group by name", (tname,))
    a = c.fetchone()
    db.close()
    return a[0]


# Средний по всем отзывам
def avgsumAll(changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("SELECT avg(mark) FROM '" + changetable + "'")
    a = c.fetchone()
    db.close()
    return a[0]


# Среднее значение тональности по фильму
def avgsumbyFilm(tfilm):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute('SELECT avg(mark) FROM usersKINO WHERE film=? group by film', (tfilm,))
    a = c.fetchone()
    db.close()
    return a[0]


# отношение если меньше, то отрицательное
# больше, положительно
# равно единица

# Отношение тональности отзывов пользователя к среднему значению по фильму
def percentFilmDeviation(tname, tfilm):
    db = lite.connect('analitics.db')
    c = db.cursor()
    debug = "SELECT avg(mark)/(SELECT avg(mark) FROM usersKINO WHERE film='" + tfilm + "' group by film)-1 FROM usersKINO WHERE (film='" + tfilm + "' and name='" + tname + "') group by name";
    c.execute(debug)
    a = c.fetchone()
    db.close()
    return a[0]


# Отношение средней тональности пользователя к среднему по общей тональности
def percentDeviation(tname, changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute(
        "SELECT avg(mark)/(SELECT avg(mark) FROM '" + changetable + "')-1 FROM '" + changetable + "' WHERE name=? group by name",
        (tname,))
    a = c.fetchone()
    db.close()
    return a[0]
