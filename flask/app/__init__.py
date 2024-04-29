import sys

sys.dont_write_bytecode = True

from flask import Flask
from flask_cors import CORS

from app.routes.admin import admin
from app.routes.ai_model import model
from app.routes.prescription import prescription


app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(admin, url_prefix="/api")
app.register_blueprint(model, url_prefix="/api")
app.register_blueprint(prescription, url_prefix="/api")


CORS(app)


if __name__ == "__main__":
    app.debug = True
    app.run()
