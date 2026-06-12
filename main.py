from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description = 'ID of the patient', example = 'P001')]
    name: Annotated[str, Field(..., description = 'Name of the patient')]
    city: Annotated[str, Field(..., description = 'City of the patient')]
    age: Annotated[int, Field(..., gt = 0, lt = 110, description = 'Age of the patient')]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description = 'Gender of the patient')]
    height: Annotated[float, Field(..., gt = 0, description = 'Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal weight'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

app = FastAPI()

# load data
def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

# save data
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

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

# add new patient record
@app.post('/create')
def create_patient(patient: Patient):
    
    # load existing data
    data = load_data()

    # check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = f"Patient with ID {patient.id} already exists")

    # add new patient to data
    data[patient.id] = patient.model_dump(exclude = ['id'])

    # save into data
    save_data(data)

    # return success message with patient id
    return JSONResponse(status_code = 201, content = {'message': f"Patient with ID {patient.id} created successfully"})