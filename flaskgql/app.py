from flask import Flask
import os

def create_app(config_override=None):    

    app = Flask(__name__, instance_relative_config=True)

    
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if config_override:
        app.config.update(config_override)


    return app    


#modules

