import sys

from app.utils.error import Error

sys.dont_write_bytecode = True

from flask import Blueprint

from app.blockchain.init import is_connected
from app.controllers.admin import add_doctor, get_all_doctors


admin = Blueprint("admin", __name__)


@admin.before_request
def check_blockchain():
    connected = is_connected()
    if not connected:
        return Error("Failed", "Blockchain Not Connected")

admin.route("/getAllDoctors", methods=["GET"])(get_all_doctors)
admin.route("/addDoctors", methods=["POST"])(add_doctor)
