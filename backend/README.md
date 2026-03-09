# Plant Health Monitoring System - Backend API

A Flask-based REST API for AI-driven plant health monitoring using machine learning to predict plant health status based on environmental and sensor data.

## 🚀 Features

- **Machine Learning**: RandomForest classifier for plant health prediction
- **Authentication**: JWT-based user authentication with role-based access control
- **Report Generation**: Automated PDF report generation with ReportLab
- **User Management**: Admin dashboard for managing users and predictions
- **Rate Limiting**: Protection against API abuse
- **MongoDB Integration**: Scalable NoSQL database for data persistence
- **CORS Support**: Configurable cross-origin resource sharing

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB 4.4 or higher
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShabeehaSarook/AI-Driven-Plant-Health-System.git
cd AI-Driven-Plant-Health-System/backend
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Change SECRET_KEY in production!
```

### 5. Set up MongoDB

Make sure MongoDB is running on your system:

```bash
# Check if MongoDB is running
mongosh --eval "db.version()"

# If not installed, install MongoDB Community Edition
# Visit: https://www.mongodb.com/try/download/community
```

### 6. Train the ML model

```bash
python scripts/train_model.py
```

This will create `ml_models/plant_model.pkl` and `ml_models/plant_model.meta.json`.

## 🏃‍♂️ Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

### Production Mode

```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key

# Run with gunicorn (recommended for production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── extensions.py         # Flask extensions
│   ├── routes/               # API endpoints
│   │   ├── auth_routes.py    # Authentication endpoints
│   │   ├── admin_routes.py   # Admin endpoints
│   │   └── prediction_routes.py  # Prediction endpoints
│   ├── services/             # Business logic
│   │   ├── ml_service.py     # ML model service
│   │   └── prediction_service.py  # Prediction service
│   ├── utils/                # Utility functions
│   │   ├── auth.py           # JWT authentication
│   │   ├── db.py             # Database operations
│   │   ├── validation.py     # Input validation
│   │   ├── report_generator.py  # PDF generation
│   │   └── ...
│   └── models/               # Data models (future)
├── config/
│   └── settings.py           # Configuration classes
├── data/
│   └── plant_health_data.csv # Training dataset
├── ml_models/                # Trained ML models
├── reports/                  # Generated PDF reports
├── scripts/
│   └── train_model.py        # Model training script
├── .env.example              # Environment template
├── .gitignore
├── requirements.txt
├── run.py                    # Application entry point
└── README.md
```

## 🔌 API Endpoints

### Authentication

- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token

### Predictions

- `POST /predict` - Make a plant health prediction (requires authentication)
- `GET /history` - Get prediction history (requires authentication)
- `POST /predictions/<id>/report/regenerate` - Regenerate PDF report
- `GET /reports/<filename>` - Download PDF report

### Admin (requires admin role)

- `GET /admin/predictions` - Get all predictions
- `POST /admin/predictions` - Create prediction manually
- `PUT /admin/predictions/<id>` - Update prediction
- `DELETE /admin/predictions/<id>` - Delete prediction

## 📝 API Usage Examples

### Register a User

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "username": "john_doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Make a Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "Plant_ID": 1,
    "Soil_Moisture": 45.5,
    "Ambient_Temperature": 25.3,
    "Soil_Temperature": 22.1,
    "Humidity": 65.2,
    "Light_Intensity": 800,
    "Soil_pH": 6.5,
    "Nitrogen_Level": 30,
    "Phosphorus_Level": 25,
    "Potassium_Level": 35,
    "Chlorophyll_Content": 45.8,
    "Electrochemical_Signal": 0.75
  }'
```

## ⚙️ Configuration

Edit the `.env` file to configure:

- **SECRET_KEY**: JWT secret (CHANGE IN PRODUCTION!)
- **MONGODB_URI**: MongoDB connection string
- **CORS_ORIGINS**: Allowed frontend origins
- **JWT_EXPIRES_HOURS**: Token expiration time
- **REPORT_RETENTION_DAYS**: How long to keep PDF reports

## 🔒 Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Role-based access control (user/admin)
- Rate limiting on sensitive endpoints
- Input validation and sanitization
- CORS protection

## 🧪 Testing

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📊 ML Model Information

- **Algorithm**: RandomForest Classifier
- **Features**: 12 environmental and sensor metrics
- **Output**: Plant health status (Healthy/Unhealthy/At Risk)
- **Confidence**: Probability-based confidence scores

### Input Features

1. Plant_ID
2. Soil_Moisture (%)
3. Ambient_Temperature (°C)
4. Soil_Temperature (°C)
5. Humidity (%)
6. Light_Intensity (lux)
7. Soil_pH
8. Nitrogen_Level (ppm)
9. Phosphorus_Level (ppm)
10. Potassium_Level (ppm)
11. Chlorophyll_Content (SPAD)
12. Electrochemical_Signal (V)

## 🐛 Troubleshooting

### MongoDB Connection Error

```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod
```

### Model Not Found Error

```bash
# Train the model first
python scripts/train_model.py
```

### Import Errors

```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For issues and questions, please open an issue on GitHub or contact the maintainers.

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
