from flask import Flask, render_template
import json
from data_model import DB, User, Tweet


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

    @app.route('/products')
    def products():
        new_tweet = Tweet(id=1, text='tweet', user_id=1)
        DB.session.add(new_tweet)
        DB.session.commit()
        return render_template('base.html', title="Products", body="products in the body")

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=8888)
