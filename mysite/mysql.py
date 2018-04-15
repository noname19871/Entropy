import sqlite3 as lite

#Создание бд
def createDB():
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("""CREATE TABLE usersKINO
             (id integer NOT NULL  primary key ,
             name text,
             film text,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE usersTWI
             (id integer NOT NULL  primary key ,
             name text,
             review text,
             mark int)""")
    c.execute("""CREATE TABLE usersENG
             (id integer NOT NULL  primary key ,
             name text,
             review text,
             mark int)""")
    db.commit()
    db.close()

#Новая запись: для кинопоиска Входные данные ('человек','plohie parni','ochen krutoi film',1,'20.10.2012')
#Для твиттера и англа 4 на вход без фильма
def newRec(inRec,changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    if (changetable in ["usersKINO"]):
        c.execute("INSERT INTO '" + changetable + "' (name, film, review, mark) VALUES (?,?,?,?)", inRec)
    else:
        c.execute("INSERT INTO '" + changetable + "' (name, review, mark) VALUES (?,?,?)", inRec)
    db.commit()
    db.close()

#Средняя по имени пользователя
def avgsumbyName(tname,changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("SELECT avg(mark) FROM '" + changetable + "' WHERE name=? group by name", (tname,))
    a = c.fetchone()
    db.close()
    return a[0]

#Средний по всем отзывам
def avgsumAll(changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("SELECT avg(mark) FROM '" + changetable + "'")
    a = c.fetchone()
    db.close()
    return a[0]

#Среднее значение тональности по фильму
def avgsumbyFilm(tfilm):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute('SELECT avg(mark) FROM usersKINO WHERE film=? group by film', (tfilm,))
    a = c.fetchone()
    db.close()
    return a[0]


#отношение если меньше, то отрицательное
#больше, положительно
#равно единица

#Отношение тональности отзывов пользователя к среднему значению по фильму
def percentFilmDeviation(tname, tfilm):
    db = lite.connect('analitics.db')
    c = db.cursor()
    debug = "SELECT avg(mark)/(SELECT avg(mark) FROM usersKINO WHERE film='" + tfilm +"' group by film)-1 FROM usersKINO WHERE (film='" + tfilm + "' and name='" + tname + "') group by name";
    c.execute(debug)
    a = c.fetchone()
    db.close()
    return a[0]

#Отношение средней тональности пользователя к среднему по общей тональности
def percentDeviation(tname,changetable):
    db = lite.connect('analitics.db')
    c = db.cursor()
    c.execute("SELECT avg(mark)/(SELECT avg(mark) FROM '" + changetable + "')-1 FROM '" + changetable + "' WHERE name=? group by name", (tname,))
    a = c.fetchone()
    db.close()
    return a[0]



createDB() #ТОЛЬКО ОДИН РАЗ ДЛЯ СОЗДАНИЯ
newRec(('человек','plohie parni','ochen krutoi film',1),'usersKINO')
newRec(('bitch','plohie parni','neochen krutoi film',3),'usersKINO')
newRec(('собака','Лунный свет','film pro geiskuu paru',5),'usersKINO')
print(avgsumbyName("bitch",'usersKINO'))
print(avgsumbyName("собака",'usersKINO'))
print(avgsumAll('usersKINO'))
print(percentDeviation("собака",'usersKINO'))
print(avgsumbyFilm('plohie parni'))
print(percentFilmDeviation("человек","plohie parni"))

newRec(('человек','ochen krutoi film',1),'usersTWI')
newRec(('bitch','neochen krutoi film',3),'usersTWI')
newRec(('собака','film pro geiskuu paru',5),'usersTWI')
print(avgsumbyName("bitch",'usersTWI'))
print(avgsumbyName("собака",'usersTWI'))
print(avgsumAll('usersTWI'))
print(percentDeviation("собака",'usersTWI'))
print(avgsumbyFilm('plohie parni'))
print(percentFilmDeviation("человек","plohie parni"))

newRec(('человек','ochen krutoi film',1),'usersENG')
newRec(('bitch','neochen krutoi film',3),'usersENG')
newRec(('собака','film pro geiskuu paru',5),'usersENG')
print(avgsumbyName("bitch",'usersENG'))
print(avgsumbyName("собака",'usersENG'))
print(avgsumAll('usersENG'))
print(percentDeviation("собака",'usersENG'))
print(avgsumbyFilm('plohie parni'))
print(percentFilmDeviation("человек","plohie parni"))
