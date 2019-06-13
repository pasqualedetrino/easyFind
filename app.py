from flask import Flask , render_template, sessions
from flask import request
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import insertDB

app = Flask(__name__)


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



@app.route('/showSignUp')
def showSignUp():
    return render_template('home.html')



dropzone = Dropzone(app)
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'


# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/showHome')
def showHome():
    return insertDB.home()

from flask_restplus import Api, Resource
import ApiUser
api = Api()
api.init_app(app)

@api.route('/prodottoCitta/<citta>/<nomeProdotto>')
class prodottoCitta(Resource):
    def get(self, citta, nomeProdotto):
        return ApiUser.ProdottoComune(citta, nomeProdotto)


@api.route('/prodottoCoordinate/<nomeProdotto>/<lat>/<long>/<raggio>')
class prodottoCoordinate(Resource):
    def get(self, nomeProdotto, lat, long, raggio):
        return ApiUser.ProdottoComunePosizione(nomeProdotto, lat, long, raggio)