from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Insurance_Premium_Prediction.schema.user_input import UserInput
from Insurance_Premium_Prediction.model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

# human readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status' : 'OK',
        'version' : MODEL_VERSION,
        'model_loaded' : model is not None
    }

# prediction endpoint
@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = {
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }

    prediction = predict_output(input_df)
    return JSONResponse(status_code = 200, content = {'prediction_category' : prediction})