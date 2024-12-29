from flask import Flask
from flask_cors import CORS

def create_app():
  app = Flask(__name__)

  # 특정 도메인만 CORS 허용
  CORS(app, resources={
    r"/*": {  
        "origins": [
          "https://poeregexkr.web.app",
          "http://localhost:3000",
        ]
    }
  })

  @app.route('/')
  def index():
    return 'test', 200

  from apps.poe2api import views as poe2api_views

  app.register_blueprint(poe2api_views.bp)

  return app