import sqlalchemy as db
import json

# SELECT OGGETTO.NOME_V, OGGETTO.PREZZO, OGGETTO.QUANTITA, VENDITORE.LAT, VENDITORE.LONG
# FROM VENDITORE JOIN PRODOTTO JOIN OGGETTO
# WHERE VENDITORE.CITTA == CITTA && PRODOTTO.NOME == NOME

def ProdottoComune(citta, nomeProdotto):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    venditore = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    query = db.select([oggetto.columns.prezzo, oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long ])
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

    query = db.select([oggetto.columns.prezzo, oggetto.columns.quantita, oggetto.columns.nome_v, venditore.columns.lat, venditore.columns.long ])
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

    return json.dumps([dict(r) for r in list])