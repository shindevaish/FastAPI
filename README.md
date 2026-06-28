## FastAPI Project

This repository contains two FastAPI-based projects:

- **Patient Management System** using `main.py` and `patients.json`
- **Insurance Premium Prediction System** using a trained ML model and FastAPI

## Project Highlights

- Built while learning **FastAPI**
- Implements **CRUD operations** for patient data
- Uses a **trained machine learning model** for insurance premium prediction
- Includes **Pydantic schemas** for request and response validation
- Supports **Docker-based deployment**

## Project Structure

- `main.py` — Patient Management System API
- `patients.json` — stores patient records
- `Insurance_Premium_Prediction/` — insurance premium prediction project
- `Insurance_Premium_Prediction/model/model.pkl` — trained ML model
- `Insurance_Premium_Prediction/model/predict.py` — model prediction logic
- `Insurance_Premium_Prediction/schema/` — request/response schemas
- `Insurance_Premium_Prediction/config/city_tier.py` — config/helper file
- `app.py` — FastAPI application
- `frontend.py` — frontend or testing script
- `fastapi_ml_model.ipynb` — notebook used for training the model
- `insurance.csv` — dataset used for training
- `Dockerfile` — containerization file
- `requirements.txt` — project dependencies

## Main Features

### Patient Management System
- Add patient details
- View all patients
- Update patient records
- Delete patient records

### Insurance Premium Prediction
- Accept user input through API
- Predict insurance premium using trained ML model
- Return prediction response in structured format

## Technologies Used

- **FastAPI**
- **Python**
- **Pydantic**
- **Machine Learning**
- **Docker**
- **JSON**
- **Jupyter Notebook**

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Docker

```bash
docker build -t fastapi-project .
docker run -p 8000:8000 fastapi-project
```

## Conclusion

This project helped me learn **FastAPI**, **ML model integration**, and **Docker-based deployment**.