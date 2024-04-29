import sys, os, json
from pathlib import Path


sys.dont_write_bytecode = True

from web3 import Web3
from app.ai.init import load_model

from dotenv import load_dotenv
load_dotenv()
 
w3 = None
network_id = None
doctor_contract = None
prescription_contract = None

def load_contract():
    global doctor_contract, prescription_contract
    doctor_contract_abi_file = os.path.join(os.path.dirname(__file__), "contractsData", "DoctorDetailContract.json")
    prescription_contract_abi_file = os.path.join(os.path.dirname(__file__), "contractsData", "PrescriptionDetailContract.json")
    doctor_contract_address_file = os.path.join(os.path.dirname(__file__), "contractsData" , "DoctorDetailContract_address.json")
    
    prescription_contract_address_file = os.path.join(os.path.dirname(__file__), "contractsData", "PrescriptionDetailContract_address.json")
    with open(doctor_contract_abi_file, 'r') as contract:
        contract_abi = json.load(contract)
    doctor_details_contract_abi = contract_abi["abi"]
    with open(doctor_contract_address_file, 'r') as contract_address:
        contract_address = json.load(contract_address)
    doctor_details_contract_address = contract_address['address']
    doctor_contract = w3.eth.contract(address = doctor_details_contract_address, abi = doctor_details_contract_abi)
    
    with open(prescription_contract_abi_file, 'r') as contract:
        contract_abi = json.load(contract)
    prescription_details_contract_abi = contract_abi["abi"]
    with open(prescription_contract_address_file, 'r') as contract_address:
        contract_address = json.load(contract_address)
    prescription_details_contract_address = contract_address['address']
    
    prescription_contract = w3.eth.contract(address = prescription_details_contract_address, abi = prescription_details_contract_abi)

def is_connected():
    global w3, network_id
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_IP")))
        network_id = str(w3.eth.chain_id)
        if doctor_contract is None and prescription_contract is None:
            load_contract()
            load_model()
        return True
    except ConnectionError as e:
        return False  
    except TimeoutError as e:
        return False 
    except Exception as e:
        print(e)
        return False
    
