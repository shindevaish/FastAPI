from fastapi import FastAPI, Path, HTTPException, Query
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
    raise HTTPException(status_code = 404, detail = f"Patient with ID {patient_id} not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = 'Sort on the basis of height, weight or bmi'), sort_order: str = Query('asc', description = 'Sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")

    if sort_order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = f"Invalid order. Select between asc or desc")

    data = load_data()
    order = True if sort_order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = order)

    return sorted_data