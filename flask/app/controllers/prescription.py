from dotenv import load_dotenv
load_dotenv()
 
from flask import  jsonify, request, send_file
from app.utils.success import Success
from app.utils.error import Error
import app.blockchain.init
import sys, os
import qrcode
from web3.middleware import geth_poa_middleware
import numpy as np
from zxing import BarCodeReader
import cv2
sys.dont_write_bytecode = True

def add_prescription():
    try:
        values = list(request.json.values())

        w3 = app.blockchain.init.w3
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        account = os.getenv("ADMIN_ACCOUNT")
        prescriptionDetailContract = app.blockchain.init.prescription_contract
        transaction_hash = prescriptionDetailContract.functions.addPrescription({
            "name": values[0],
            "email": values[1],
            "disease" : values[2],
            "prescription" : values[3],
            "comments" : values[4]
        }
        ).transact({
            "from": account
        })
        # print(transaction_hash.hex())
        success = True
        data_to_encode = transaction_hash.hex()

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_encode)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")        
        img.save("qrcode.png")
    except Exception as e:
        print(e)
        return Error("Failed", str(e), 200)
    if success:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image = os.path.join(current_directory, '..', '..', 'qrcode.png')
        return send_file(image, mimetype='image/jpg')

    return Error("Failed", "Prescription not Added")


def get_all_prescription():
    all_prescriptions = []
    prescriptionDetailContract = app.blockchain.init.prescription_contract
    doctorCount = prescriptionDetailContract.functions.prescriptionCount().call()
    for i in range(doctorCount):     
        all_prescriptions.append(prescriptionDetailContract.functions.prescription(i).call())

    return Success("Success", all_prescriptions)


def decodeQRCode():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    img = request.files['image']
    img_array = np.frombuffer(img.read(), np.uint8)
    
    # Decode the NumPy array as an image using OpenCV
    img_cv2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Now you can use img_cv2 as a variable containing the image data
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img_cv2)

    try:
        def decodeInputData(w3, transactionHash, contract):
            transaction = w3.eth.get_transaction(transactionHash)
            decoded_input = contract.decode_function_input(transaction["input"])
            return (decoded_input[1]['_prescription'])

        w3 = app.blockchain.init.w3
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        prescriptionDetailContract = app.blockchain.init.prescription_contract
        res = decodeInputData(w3, data, prescriptionDetailContract)
        result = {
            "hash" : data,
            "data" : res
        }
        return Success("Success",result)
    except Exception as e:
        print(e)
        result = {
            "hash" : None
        }
        return Error("Failure",result)