import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from sklearn.preprocessing import LabelEncoder

def main():
    st.title("CHLA Predictor")
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">CHLA No Show Predictor App </h2>
    </div>
    """

    # Bringing in CHLA data
    reference_df = pd.read_csv('CHLA_clean_data_until_2023.csv')
    reference_df['APPT_DATE'] = pd.to_datetime(reference_df['APPT_DATE'])

    max_df_date = max(reference_df['APPT_DATE'])
    min_df_date = min(reference_df['APPT_DATE'])

    st.markdown(html_temp, unsafe_allow_html = True)

    START_DATE  = st.date_input("Start date", 
                           value=None, 
                           min_value=min_df_date, 
                           max_value=max_df_date, 
                           key="start_date")
    END_DATE  = st.date_input("End date", 
                           value=None, 
                           min_value=pd.Timestamp(START_DATE) if START_DATE else min_df_date, 
                           max_value=max_df_date, 
                           key="end_date")

    #backend API URL

    url = "http://127.0.0.1:8000/predict/"

    if st.button("Predict"):

       # Send request to backend API
        response = requests.post(url, json={"start_date": START_DATE.isoformat(), "end_date": END_DATE.isoformat()})

        # After receiving the response from back-end API
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.write(prediction)
        else:
            st.error("Error in backend processing.")

if __name__ == '__main__':
    main()
