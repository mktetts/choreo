## Running Flask app

1. Install requirements
```
pip install -r requirements.txt
```
2. Fill up the .env file
3. Run this command
```
flask run
```

### APIs provided

* /api/addDoctors 
> Fields:
> {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com",
    "qualification": "MD",
    "hospital": "General Hospital",
    "specialist": "Cardiology",
    "phone": "+1234567890",
    "password": optional
}

* /api/getAllDoctors
> Returns all Doctors list

* /api/addPrescription
> Fields
> {
    "PrescribedBy": "Dr. Smith",
    "DoctorsEmail": "dr.smith@example.com",
    "Disease": "Influenza",
    "Prescription": "Take two tablets of ibuprofen every 6 hours.",
    "Comments": "Get plenty of rest and drink fluids."
}

* /api/getAllPrescription
> Returns all Prescription list

* /api/decodeQRCode
> Input : QR code
> Output : Decoded Transaction Information

* /api/predictPrescription
> Input : Prescription Image
> Output : Predicts the Doctor's Prescription Medicines

* /api/predictWound
> Input : Wound Image
> Output : Predicts the Patients wound type

* /api/questionAnswering
> Input : Query prompt
> Output : Answer for the query