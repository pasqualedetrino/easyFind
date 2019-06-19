import sqlalchemy as db
from flask import render_template , redirect, url_for
import app
import json
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def home(nome, categoria):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    prod = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    print('---CATEGORIA', categoria)
    if categoria is None:
        dizionario = {'nome':nome, 'nome_prod': [], 'id': [], 'cat_scelta': categoria}
    else:
        query3 = db.select([prod.columns.nome_prodotto.distinct(), prod.columns.nome_img]).where(prod.columns.categoria == categoria)
        ris = connection.execute(query3)
        ResultSet = ris.fetchall()
        dizionario = {'nome':nome, 'nome_prod': [], 'id': [], 'cat_scelta': categoria}
        lista = []
        listId = []
        i = 0
        for var in ResultSet:
            lista.insert(i, var[0])
            listId.insert(i,var[1])
            i = i + 1
        dizionario['nome_prod'] = lista
        dizionario['id'] = listId
        print('lista: ' + str(lista))
        print('dizionario: ' + str(dizionario))

    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    mieiProd = db.select([oggetto, prod])
    mieiProd = mieiProd.select_from(oggetto.join(prod, oggetto.columns.id_prodotto == prod.columns.id))
    mieiProd = mieiProd.where(oggetto.columns.nome_v == nome.upper() )

    ris = connection.execute(mieiProd).fetchall()

    prodMiei = json.dumps([dict(r) for r in ris])
    print('PRODOTTIMIEI ' + prodMiei)

    Qcategorie = db.select([prod.columns.categoria.distinct()])
    categorie = connection.execute(Qcategorie).fetchall()

    categoriePresenti = json.dumps([dict(r) for r in categorie])
    return render_template("home.html", message=dizionario, risposta=prodMiei, category=categoriePresenti)


def insert_prod(categoria,nome,n_img):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    prod = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    query = db.select([db.func.max(prod.columns.id)])
    ris = connection.execute(query).fetchall()
    maxIdProd = ris[0][0]
    if n_img and allowed_file(n_img.filename):
        nome_im = app.secure_filename(str(int(maxIdProd) + 1)+'.'+n_img.filename.rsplit('.', 1)[1].lower())
        path_img=app.os.path.join(app.app.config['UPLOAD_FOLDER'], nome_im)
        n_img.save(path_img)
        query2 = db.insert(prod).values(id=int(maxIdProd) + 1, categoria=categoria.upper(), nome_prodotto=nome.upper(), nome_img=nome_im)
        connection.execute(query2)
    else:
        print('File non concesso!')
    return

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
    val_hash = app.hashing.hash_value(password, salt='geo')
    query2 = db.insert(emp).values(nome=nome.upper(), password=val_hash, citta=citta.upper(), indirizzo = indirizzo.upper(), lat=lat, long=long)
    connection.execute(query2)
    app.login_user(app.User(nome))
    return redirect('/Home_page')


def access(nome, password):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()
    emp = db.Table('venditore', metadata, autoload=True, autoload_with=engine)
    query = db.select([emp.columns.nome, emp.columns.password]).where(db.and_(emp.columns.nome == nome.upper()))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if (len(ResultSet) == 1):
        if app.hashing.check_value(ResultSet[0][1], password, salt='geo'):
            app.login_user(app.User(nome))
            return redirect('/Home_page')
    return render_template('index.html', error={'value': 'error_login'})


def insertOggetto(nomeProdotto, quantita, prezzo, nome):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    query = db.select([db.func.max(oggetto.columns.id_oggetto)]) # ultimo id dell' oggetto
    ris = connection.execute(query).fetchall()
    maxIdOgg = ris[0][0]
    if maxIdOgg  is None:
        maxIdOgg = 0

    print(nomeProdotto)
    query2 = db.select([prodotto.columns.id]).where(prodotto.columns.nome_prodotto == nomeProdotto.upper() )
    idP = connection.execute(query2).fetchall()
    print(idP)
    idProdotto = idP[0][0]

    query3 = db.insert(oggetto).values(id_oggetto = int(maxIdOgg)+1, nome_v = nome.upper(), id_prodotto = int(idProdotto), quantita = int(quantita), prezzo = float(prezzo))
    connection.execute(query3)

    print('ho iserito!')
    return redirect("/Home_page")

def modificaOggetto(mioId_ogg, mioProdotto, miaQuantita):
    engine = db.create_engine('sqlite:///easyFindDB.db')
    connection = engine.connect()
    metadata = db.MetaData()

    prodotto = db.Table('prodotto', metadata, autoload=True, autoload_with=engine)
    oggetto = db.Table('oggetto', metadata, autoload=True, autoload_with=engine)

    idogg = db.select([prodotto.columns.id]).where(prodotto.columns.nome_prodotto == mioProdotto.upper() )
    risultato = connection.execute(idogg).fetchall()
    idProd = risultato[0][0]

    print('----mioProdotto ' + mioProdotto)
    print('----miaQuantita ' + miaQuantita)
    print(idProd)

    if int(miaQuantita)>0:
        modifica = db.update(oggetto).values(quantita = int(miaQuantita)).where(db.and_(oggetto.columns.id_prodotto == idProd, oggetto.columns.id_oggetto == mioId_ogg))
        connection.execute(modifica)
        print('ho modificato!')
    else:
        elimina = db.delete(oggetto).where(db.and_(oggetto.columns.id_prodotto == idProd, oggetto.columns.id_oggetto == mioId_ogg))
        connection.execute(elimina)
        print('ho eliminato!')


    return redirect("/Home_page")
