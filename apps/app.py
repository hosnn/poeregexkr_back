from flask import Flask
from flask_cors import CORS

def create_app():
  app = Flask(__name__)

  CORS(app)

  from apps.poe2api import views as poe2api_views

  app.register_blueprint(poe2api_views.bp)

  return app