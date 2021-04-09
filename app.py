from flask import Flask, render_template, request
import json
from data_model import DB, User, Tweet
from twitter import upsert_user


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def landing():
        DB.drop_all()
        DB.create_all()
        app_user = User(id=1, name='app_user')
        DB.session.add(app_user)
        DB.session.commit()
        with open('templates/landing.json') as f:
            args = json.load(f)
        return render_template('base.html', **args)

    @app.route('/add_user', methods=['GET'])
    def add_user():
        twitter_handle = request.args['twitter_handle']
        upsert_user(twitter_handle)
        return 'insert successful'

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=8888)
