import sqlalchemy as db
import json

# trovare i venditori che vendono un dato prodotto in una data città
# restituisce il venditore, il prezzo, la quantità, l'indirizzo, le coordinate del venditore

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


# trovare i venditori entro un certo raggio dalla posizione dell'utente che vendono un dato prodotto
# restituisce il venditore, il prezzo, la quantità, l'indirizzo, le coordinate del venditore

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

# trovare il venditore che vende un dato prodotto al miglior prezzo entro una certa posizione
# restituisce il venditore, il prezzo, la quantità, l'indirizzo, le coordinate del venditore

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


# conoscere le categorie presenti nel sistema

def CategoriePresenti():
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.categoria])

    result = connection.execute(query).fetchall()

    return json.dumps([dict(r) for r in result])

# conoscere i prodotti di una specifica categoria

def ProdottiCategoria(categoria):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)

    query = db.select([prodotto.columns.nome_prodotto])
    query = query.where(prodotto.columns.categoria == categoria)

    result = connection.execute(query).fetchall()

    return json.dumps([dict(r) for r in result])
