import sqlalchemy as db
import json
import sys


def ProdottoComune(citta, nomeProdotto):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    venditore = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    query = db.select([oggetto.columns.prezzo, oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long, venditore.columns.indirizzo ])
    query = query.select_from(prodotto.join(oggetto.join(venditore, oggetto.columns.nome_v == venditore.columns.nome),oggetto.columns.id_prodotto == prodotto.columns.id))
    query = query.where(db.and_(venditore.columns.citta == citta, prodotto.columns.nome_prodotto == nomeProdotto) )
    result = connection.execute(query).fetchall()

    dizionario = {'item': []}
    lista = []

    i = 0
    for var in result:
        elem = {"nome_v": var[2], "prezzo": var[0], "indirizzo": var[5], "quantita": var[1]}
        lista.insert(i, elem)

        i = i + 1
    dizionario['item'] = lista

    return dizionario

from geopy.distance import geodesic



def ProdottoComunePosizione(nomeProdotto, lat, long, raggio):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    venditore = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    query = db.select([oggetto.columns.prezzo, oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long, venditore.columns.indirizzo ])
    query = query.select_from(prodotto.join(oggetto.join(venditore, oggetto.columns.nome_v == venditore.columns.nome),oggetto.columns.id_prodotto == prodotto.columns.id))
    query = query.where(prodotto.columns.nome_prodotto == nomeProdotto)
    result = connection.execute(query).fetchall()

    posCliente = (lat, long)
    list = []

    for var in result:
        negozio = (var[3], var[4])

        dist = geodesic(posCliente, negozio).kilometers

        if dist < int(raggio):
            print(dist)
            list.append(var)

    return json.dumps([dict(r) for r in list])



def ProdottoComunePosizionePrezzo(nomeProdotto, lat, long, raggio):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    venditore = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    query = db.select([oggetto.columns.prezzo, oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long, venditore.columns.indirizzo ])
    query = query.select_from(prodotto.join(oggetto.join(venditore, oggetto.columns.nome_v == venditore.columns.nome),oggetto.columns.id_prodotto == prodotto.columns.id))
    query = query.where(prodotto.columns.nome_prodotto == nomeProdotto)
    result = connection.execute(query).fetchall()

    posCliente = (lat, long)

    dizionario = {'item': []}
    lista = []

    i = 0
    for var in result:
        negozio = (var[3], var[4])

        dist = geodesic(posCliente, negozio).kilometers

        if dist < int(raggio):
            elem = {"nome_v": var[2], "prezzo": var[0], "indirizzo": var[5], "quantita": var[1]}
            lista.insert(i, elem)
            i = i + 1

    dizionario['item'] = lista

    return dizionario

def CategoriePresenti():
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.categoria.distinct()])

    result = connection.execute(query).fetchall()

    dizionario = {'item': [] }
    lista = []


    i = 0
    for var in result:
        elem = {"categoria": var[0]}
        lista.insert(i, elem)

        i = i + 1
    dizionario['item'] = lista

    return dizionario



def ProdottiCategoria(categoria):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.nome_prodotto])
    query = query.where(prodotto.columns.categoria == categoria)

    result = connection.execute(query).fetchall()

    dizionario = {'item': [] }
    lista = []


    i = 0
    for var in result:
        elem = {"nome_prodotto": var[0]}
        lista.insert(i, elem)

        i = i + 1
    dizionario['item'] = lista

    return dizionario
