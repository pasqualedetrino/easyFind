from flask import Flask , render_template, redirect
import insertDB
import os
from flask import Flask
from flask_hashing import Hashing
from flask import Flask,request,session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug import secure_filename

app = Flask(__name__)
app.config['HASHING_METHOD'] = 'sha384'

hashing = Hashing(app)
hashing.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''
app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah"
app.config [ 'UPLOAD_FOLDER'] = 'static/prodotti'
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):
  def __init__(self,id):
    self.id = id

  def get_name(self):
        return self.id


if __name__ == '__main__':
    app.run()

@app.route('/')
def main():
    return render_template('index.html', error = {'value' : 'false'})


@app.route('/signUp', methods=('GET', 'POST'))
def signUp():
    if request.method == 'POST':
        name = request.form.get('nome')
        password = request.form.get('password')
        citta = request.form.get('citta')
        indirizzo = request.form.get('indirizzo')
        lat = float(request.form.get('lat'))
        long = float(request.form.get('long'))
        return (insertDB.insert(name, password, citta, indirizzo, lat, long))

@app.route('/signIn', methods=('GET', 'POST'))
def signIn():
    if request.method == 'POST':
        name = request.form.get('form-username')
        password = request.form.get ('form-password')
        return (insertDB.access(name, password))


@app.route('/Home_page')
@login_required
def Home_page():
    username = current_user.get_name()
    return insertDB.home(username, None, "unsuccessful")


@app.route('/insertOgg', methods=('GET', 'POST'))
@login_required
def insertOgg():
    if request.method == 'POST':
        nomeProdotto = request.form.get('articolo')
        quantita = request.form.get('quantita')
        prezzo = request.form.get('prezzo')
        nome = current_user.get_name()
        return (insertDB.insertOggetto(nomeProdotto, quantita, prezzo, nome) )

@app.route('/myOgg', methods=('GET', 'POST') )
@login_required
def myOgg():
    if request.method == 'POST':
        mioIdOgg = request.form.get('mioId_ogg')
        mioArticolo = request.form.get('mioArticolo')
        miaQuantita = request.form.get('miaQuantita')
        print('mioIdOgg ' + mioIdOgg)
        print('mioArticolo ' + mioArticolo)
        print('miaQuantita ' + miaQuantita)
        return (insertDB.modificaOggetto(mioIdOgg, mioArticolo, miaQuantita) )

@app.route('/setCategoria', methods=('GET', 'POST'))
@login_required
def get_post_javascript_data():
    jsdata = request.form['cat']
    print('jsondata ' + jsdata)
    username = current_user.get_name()
    return insertDB.home(username, jsdata, "unsuccessful")

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
    return  redirect('/indexOut')

@app.route('/indexOut')
def indexOut():
    return render_template('index.html', error = {'value' : 'disconnect'})


@app.route('/uploader', methods=('GET', 'POST'))
@login_required
def upload_file():
   print("ook");
   if request.method == 'POST':
      f = request.files['file']
      categoria= request.form.get('categoria')
      nome_prod = request.form.get('nome_prodotto')
      boolRis = insertDB.insert_prod(categoria,nome_prod,f)
      if boolRis == True:
          return  redirect('HomePage')
      else:
          return  redirect('Home-Page')

@app.route('/HomePage')
@login_required
def HomePage():
   username = current_user.get_name()
   return insertDB.home(username, None, "success")

@app.route('/Home-Page')
@login_required
def HomePag():
   username = current_user.get_name()
   return insertDB.home(username, None, "ridondante")