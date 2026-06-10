from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import json


class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description = 'ID of the patient', example = 'P001')]
    name: Annotated[str, Field(..., description = 'Name of the patient')]
    city: Annotated[str, Field(..., description = 'City of the patient')]
    age: Annotated[int, Field(..., gt = 0, lt = 120, description = 'Age of the patient')]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description = 'Gender of the patient')]
    height: Annotated[float, Field(..., gt = 0, description = 'Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Weight of the patient in kgs')]

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
def view_patient(patient_id: str = Path(..., description = 'The ID of the patient in the DB', examples = 'P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = f"Patient with ID {patient_id} not found")

# sort data by height, weight or bmi in ascending or descending order
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