from flask import Flask , render_template, redirect
import insertDB

app = Flask(__name__)

from flask import Flask,request,session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug import secure_filename
app = Flask(__name__)
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''
app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah"
app.config [ 'UPLOAD_FOLDER'] = '/static/prodotti'
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):
  def __init__(self,id):
    self.id = id



if __name__ == '__main__':
    app.run()

@app.route('/')
def main():
    return render_template('index.html', error = {'value' : 'false'})


@app.route('/signUp', methods=['POST'])
def signUp():
    if request.method == 'POST':
        name = request.form.get('nome')
        password = request.form.get('password')
        citta = request.form.get('citta')
        indirizzo = request.form.get('indirizzo')
        lat = float(request.form.get('lat'))
        long = float(request.form.get('long'))
        return (insertDB.insert(name, password, citta, indirizzo, lat, long))

@app.route('/signIn', methods=['POST'])
def signIn():
    if request.method == 'POST':
        name = request.form.get('form-username')
        password = request.form.get ('form-password')
        return (insertDB.access(name, password))


@app.route('/Home_page', methods=['GET'])
@login_required
def Home_page():
    username = request.args.get('nome')
    return insertDB.home(username)


@app.route('/insertOgg', methods=['POST'])
@login_required
def insertOgg():
    if request.method == 'POST':
        #nomeProdotto = request.form.get('bottone')
        nomeProdotto = 'salame'

        quantita = request.form.get('quantita')
        prezzo = request.form.get('prezzo')
        #print(request.form)
        #print('nome ' + nomeProdotto)
        ##print('quanti ' + quantita)
        #print('prezzo ' + prezzo)
        return (insertDB.insertOggetto(nomeProdotto, quantita, prezzo) )


# ---------------------------------------------------------------------------------------------------

from flask_restplus import Api, Resource
import ApiUser
api = Api()
api.init_app(app)

@api.route('/api/prodottoCitta/<citta>/<nomeProdotto>')
class prodottoCitta(Resource):
    def get(self, citta, nomeProdotto):
        return ApiUser.ProdottoComune(citta, nomeProdotto)

@api.route('/api/prodottoCoordinate/<nomeProdotto>/<lat>/<long>/<raggio>')
class prodottoCoordinate(Resource):
    def get(self, nomeProdotto, lat, long, raggio):
        return ApiUser.ProdottoComunePosizione(nomeProdotto, lat, long, raggio)

@api.route('/api/prodottoCoordinatePrezzo/<nomeProdotto>/<lat>/<long>/<raggio>')
class prodottoCoordinate(Resource):
    def get(self, nomeProdotto, lat, long, raggio):
        return ApiUser.ProdottoComunePosizionePrezzo(nomeProdotto, lat, long, raggio)

@api.route('/api/categorie')
class categorie(Resource):
    def get(self):
        return ApiUser.CategoriePresenti()

@api.route('/api/prodotticategoria/<categoria>')
class prodotticategoria(Resource):
    def get(self, categoria):
        return ApiUser.ProdottiCategoria(categoria)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html', error = {'value' : 'disconnect'})


@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      username = request.form.get('nome')
      categoria= request.form.get('categoria')
      nome_prod = request.form.get('nome_prodotto')
      insertDB.insert_prod(categoria,nome_prod,f.filename)
      return redirect(insertDB.url_for('Home_page', nome=username))