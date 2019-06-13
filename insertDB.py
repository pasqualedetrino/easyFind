import sqlalchemy as db
from flask import render_template , redirect

accesso = False


def home():
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    prod = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    query3 = db.select([prod.columns.nome_prodotto.distinct()])
    ris = connection.execute(query3)
    ResultSet = ris.fetchall()
    dizionario = {'nome_prod': []}
    lista = []
    i = 0
    for var in ResultSet:
        lista.insert(i, var[0])
        i = i + 1
    dizionario['nome_prod'] = lista
    print('lista: ' + str(lista))
    print('dizionario: ' + str(dizionario))
    return render_template("home.html", message=dizionario)

def insert(nome, password, citta, indirizzo, lat, long):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    emp = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    query = db.select([emp.columns.nome]).where(emp.columns.nome == nome.upper())
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if (len(ResultSet) > 0):
        return render_template('index.html', error={'value': 'error_register'})
    query2 = db.insert(emp).values(nome=nome.upper(), password=password, citta=citta.upper(), indirizzo = indirizzo.upper(), lat=lat, long=long)
    connection.execute(query2)
    return redirect("/Home_page")


def access(nome, password):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    emp = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    query = db.select([emp.columns.nome]).where(db.and_(emp.columns.nome == nome.upper(), emp.columns.password == password))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if (len(ResultSet) == 1):
        global accesso
        accesso = True
        return redirect("/Home_page")
    return render_template('index.html', error={'value': 'error_login'})
