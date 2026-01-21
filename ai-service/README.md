# Plant Health Monitoring System

AI-powered system for monitoring plant health using environmental sensor data.

## Features

- User authentication (JWT)
- Real-time plant health prediction
- ML model with 95%+ accuracy
- Downloadable PDF reports
- Prediction history
- Explainable AI results

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** React
- **Database:** MongoDB
- **ML:** scikit-learn (Random Forest)
- **Auth:** JWT + bcrypt

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB:
```bash
net start MongoDB
```

3. Train the model:
```bash
python train_model.py
```

4. Run backend:
```bash
python app.py
```

5. Run frontend:
```bash
cd frontend
npm start
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Health check | No |
| POST | `/register` | Register user | No |
| POST | `/login` | User login | No |
| POST | `/predict` | Predict plant health | Yes |
| GET | `/history` | Get predictions | Yes |
| GET | `/reports/<file>` | Download report | No |

## Usage

1. Register/Login to get JWT token
2. Input 12 plant parameters:
   - Soil Moisture, Temperature, Humidity
   - pH, NPK levels, Chlorophyll
   - Light Intensity, etc.
3. Get prediction with confidence score
4. View explanation and download PDF report

## Model Details

- **Algorithm:** Random Forest Classifier
- **Trees:** 200
- **Accuracy:** 95.2%
- **Features:** 12 environmental parameters
- **Output:** Healthy / Moderate Stress / High Stress

## Project Structure

```
├── app.py                  # Main Flask application
├── predict_api.py          # ML prediction logic
├── train_model.py          # Model training
├── routes/
│   └── auth_routes.py      # Authentication routes
├── utils/
│   ├── auth.py             # JWT authentication
│   ├── db.py               # MongoDB operations
│   ├── report_generator.py # PDF reports
│   └── ...
├── data/                   # Training data
├── models/                 # Trained ML model
└── frontend/               # React application
```

## Author

Built as a final year project for agricultural technology applications.
