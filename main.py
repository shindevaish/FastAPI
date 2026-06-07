from fastapi import FastAPI, Path
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}

@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patients records.'}

# view data
@app.get("/view")
def view():
    data = load_data()
    return data

# view data by patient id
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description = 'The ID of the patient in the DB', example = 'P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        return {'error': 'Patient not found'}