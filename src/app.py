from flask import Flask, render_template, request, redirect, url_for, flash
import routes.auth
import routes.avaliacao

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = '/uploads'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Precisa dessa chave pra mostrar flash messages

    app.register_blueprint(routes.auth.blueprint)
    app.register_blueprint(routes.avaliacao.blueprint)

    return app

if __name__ == "__main__":
    create_app().run()
