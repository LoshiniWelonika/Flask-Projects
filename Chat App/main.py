#Imports
import os
import random
import logging
from datetime import datetime
from typing import Dict

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.middleware.proxy_fix import ProxyFix


#Logging
logging.basicConfig(
    level=logging. INFO,
    format= '%(asctime)s - %(name)s - %(levelname)s -%(message)s'
)

logger = logging.getLogger(__name__)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
    DEBUG = os.environ.get("FLASK_DEBUG", "False"). lower() in ('true', "1", "t")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    #Chat Rooms
    CHAT_ROOMS = [
        "General",
        "Special",
        "Friends",
        "Official" 
    ]



app = Flask(__name__)
app.config.from_object(Config)


#Handle reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)






@app.route("/")
def index():
    return "Welcome"

if __name__ == "__main__":
    app.run(debug=True)