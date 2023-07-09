from flask import Flask, render_template, request, redirect, url_for, flash
#from database.db import Database
#import base64
from werkzeug.utils import secure_filename
import routes.auth

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = '/uploads'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Precisa dessa chave pra mostrar flash messages

    app.register_blueprint(routes.auth.blueprint)

    @app.route('/')
    def home():
        return render_template('home.html', name="Pedro")

    return app

if __name__ == "__main__":
    create_app().run()
