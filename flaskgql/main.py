from .app import create_app
from .models import db
from flask_migrate import Migrate
from .schema import init_app as init_schema

from flask_graphql_auth import GraphQLAuth

import flask_login

import os
basedir = os.path.abspath(os.path.dirname(__file__))    
config = {}

config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'data.sqlite')

# create app instance
app = create_app(config_override=config)

# jwt auth
auth = GraphQLAuth(app)

# setup db
db.init_app(app)

# setup migration
migrate = Migrate(app, db)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# setup graphql
init_schema(app)


@app.route("/")
def index():

    return "<p>Flask GraphQL!</p>"

if __name__ == '__main__':
    app.run()
