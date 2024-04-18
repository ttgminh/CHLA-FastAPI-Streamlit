# CHLA No Show Prediction App

This repository contains a web application for predicting no-show probabilities at CHLA (Children's Hospital Los Angeles). The application uses FastAPI for the backend and Streamlit for the front end, ensuring a responsive and interactive user experience.

## Architecture

- **Backend**: Built with FastAPI, handling data processing and model inference.
- **Frontend**: Developed using Streamlit, providing an interactive UI for data input and displaying predictions.

## Local Setup and Installation

Ensure you have Python installed and then follow these steps to set up both components locally:

1. **Start the FastAPI Server**:
   Open a PowerShell prompt and run the following command:
   ```bash
   uvicorn backend:app --reload
2. **Start the Streamlit Frontend:**
   Open another PowerShell prompt and execute:
   ```bash
   streamlit run frontend/app.py

## Usage

After setting up both the FastAPI backend and Streamlit frontend:

- **FastAPI Backend**: Access the API and its documentation by navigating to `http://127.0.0.1:8000/docs`. Here, you can interact directly with the backend services.
- **Streamlit Frontend**: Visit `http://localhost:8501` in your web browser. Through the user interface, input date ranges and other relevant parameters to receive predictions on appointment no-show probabilities.

## Future Improvements

- **Backend and Frontend Connection**: Enhance the integration between the backend and frontend to ensure a seamless data exchange and real-time updates.
- **Containerization**: Implement Docker containers for both the backend and frontend to simplify deployment processes and enhance scalability.
- **Facility Selection**: Introduce the ability to select different CHLA facilities within the application to provide more specific and relevant predictions based on each facility's unique data set.
