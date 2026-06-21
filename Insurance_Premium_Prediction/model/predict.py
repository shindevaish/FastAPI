import pickle
import pandas as pd

# import the ml model
with open('Insurance_Premium_Prediction/model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# MLFlow
MODEL_VERSION = '1.0.0'

# Get class labels from model
class_labels = model.classes_.tolist()

def predict_output(user_input : dict):

    input_df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(input_df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    # Create mapping
    class_proba = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted category" : predicted_class,
        "confidence" : round(confidence, 4),
        "class probabilities" : class_proba
    }