import sys

from app.utils.error import Error

sys.dont_write_bytecode = True

from app.controllers.ai_model import predictWound, predictPrescription, questionAnswering
from app.blockchain.init import is_connected
from flask import Blueprint


model = Blueprint("model", __name__)

@model.before_request
def check_blockchain():
    connected = is_connected()
    if not connected:
        return Error("Failed", "Blockchain Not Connected")
    
model.route("/predictPrescription", methods=["POST"])(predictPrescription)
model.route("/predictWound", methods=["POST"])(predictWound)
model.route("/questionAnswering", methods=["POST"])(questionAnswering)

