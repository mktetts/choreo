from dotenv import load_dotenv
load_dotenv()
 
from flask import  jsonify, request
from app.utils.success import Success
from app.utils.error import Error
import app.blockchain.init
import sys, os

from web3.middleware import geth_poa_middleware

sys.dont_write_bytecode = True


def add_doctor():
    try:
        values = list(request.json.values())
        w3 = app.blockchain.init.w3
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        account = os.getenv("ADMIN_ACCOUNT")
        doctorDetailContract = app.blockchain.init.doctor_contract
        print(doctorDetailContract)
        userPassword = values[2] + "@" + "12345"
        doctorDetailContract.functions.addDoctor({
            "name": values[0],
            "age": values[1],
            "email": values[2],
            "qualification": values[3],
            "hospital": values[4],
            "specialist": values[5],
            "phone" : values[6],
            "password" : userPassword
        }
        ).transact({
            "from": account
        })
        
        return Success("Success", "Doctor Details Successfully Added")
    except Exception as e:
        return Error("Failed", str(e))

def get_all_doctors():
    w3 = app.blockchain.init.w3
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    doctorDetailContract = app.blockchain.init.doctor_contract
    all_doctors = []
    doctorCount = doctorDetailContract.functions.doctorCount().call()
    for i in range(doctorCount):     
        all_doctors.append(doctorDetailContract.functions.doctor(i).call())
    return Success("Success", all_doctors)

def check():
    return {}