import sqlalchemy as db
import json



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

    print(result)

    return json.dumps([dict(r) for r in result])

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

    query = db.select([db.func.min(oggetto.columns.prezzo), oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long, venditore.columns.indirizzo ])
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




def CategoriePresenti():
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.categoria])

    result = connection.execute(query).fetchall()

    return json.dumps([dict(r) for r in result])



def ProdottiCategoria(categoria):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.nome_prodotto])
    query = query.where(prodotto.columns.categoria == categoria)

    result = connection.execute(query).fetchall()

    return json.dumps([dict(r) for r in result])
