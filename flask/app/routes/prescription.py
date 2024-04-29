import sys

from app.utils.error import Error

sys.dont_write_bytecode = True

from flask import Blueprint

from app.blockchain.init import is_connected
from app.controllers.prescription import add_prescription, get_all_prescription, decodeQRCode


prescription = Blueprint("prescription", __name__)


@prescription.before_request
def check_blockchain():
    connected = is_connected()
    if not connected:
        return Error("Failed", "Blockchain Not Connected")

prescription.route("/getAllPrescription", methods=["GET"])(get_all_prescription)
prescription.route("/addPrescription", methods=["POST"])(add_prescription)
prescription.route("/decodeQRCode", methods=["POST"])(decodeQRCode)
