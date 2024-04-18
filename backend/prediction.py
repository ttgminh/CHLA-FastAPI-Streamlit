from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
import warnings
from datetime import datetime

app = FastAPI()

# Ignore warnings
warnings.filterwarnings("ignore")

# Load model and encoder
try:
    model = pickle.load(open('model.pkl', 'rb'))
except Exception as e:
    raise HTTPException(status_code=500, detail="Model loading failed: " + str(e))

try:
    with open('label_encoder.pkl', 'rb') as pkl_file:
        encoder_dict = pickle.load(pkl_file)
except Exception as e:
    raise HTTPException(status_code=500, detail="Encoder dictionary loading failed: " + str(e))

class PredictionRequest(BaseModel):
    start_date: str
    end_date: str

def encode_features(df, encoder_dict):
    category_col = ['APPT_STATUS', 'ZIPCODE', 'CLINIC', 'APPT_TYPE_STANDARDIZE', 'ETHNICITY_STANDARDIZE', 'RACE_STANDARDIZE']
    for col in category_col:
        if col in encoder_dict:
            classes = encoder_dict[col]
            df[col] = df[col].apply(lambda x: classes.index(x) if x in classes else -1)  # Assign -1 for unseen categories
        else:
            df[col] = -1  # Assign -1 if the whole column is missing in the encoder
    return df

@app.post("/predict/")
async def make_prediction(request: PredictionRequest):
    # Load reference data
    try:
        reference_df = pd.read_csv('CHLA_clean_data_until_2023.csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail="Data loading failed: " + str(e))

    # Convert date columns to datetime
    reference_df['APPT_DATE'] = pd.to_datetime(reference_df['APPT_DATE'])

    # Filter data based on the requested dates
    start_date = datetime.strptime(request.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
    output_df_all = reference_df[(reference_df['APPT_DATE'] >= start_date) & (reference_df['APPT_DATE'] <= end_date)]

    # Encoding features from encoded dataset
    df = encode_features(output_df_all, encoder_dict)
    if 'APPT_DATE' in df.columns:
        features_list = df.drop(columns=['APPT_DATE']).values
    else:
        features_list = df.values

    # Prediction
    prediction = model.predict(features_list)
    output_df_all.loc[:,'PREDICTION'] = prediction

    return output_df_all[['MRN', 'APPT_DATE', 'PREDICTION']].to_dict(orient='records')

