#Imports
import os
import random
import logging
from datetime import datetime
from typing import Dict

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome"

if __name__ == "__main__":
    app.run(debug=True)