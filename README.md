# 🌱 AI-Driven Plant Health Monitoring System

An intelligent, full-stack web application that uses machine learning to monitor and predict plant health status based on real-time environmental and sensor data.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)
![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)

## 🌟 Features

### 🤖 Machine Learning
- **RandomForest Classifier** for accurate plant health prediction
- **12 Environmental Features** analysis (soil moisture, temperature, pH, nutrients, etc.)
- **Confidence Scoring** with probability-based predictions
- **Feature Importance** analysis to understand key health factors
- **What-if Simulations** to test different scenarios

### 🎨 Frontend (React)
- **Modern UI/UX** with responsive design
- **User Authentication** (Login/Register)
- **Real-time Predictions** with instant results
- **Prediction History** tracking and management
- **Admin Dashboard** for user and prediction management
- **PDF Report Downloads** with detailed analysis
- **Protected Routes** for secure access

### ⚙️ Backend (Flask)
- **RESTful API** with JWT authentication
- **MongoDB Integration** for scalable data storage
- **PDF Report Generation** using ReportLab
- **Rate Limiting** for API protection
- **Role-Based Access Control** (User/Admin)
- **Comprehensive Error Handling**
- **CORS Support** for cross-origin requests

## 📋 Table of Contents

- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [ML Model Details](#-ml-model-details)
- [Contributing](#-contributing)
- [License](#-license)

## 🎥 Demo

### Prediction Workflow
1. User inputs 12 environmental parameters
2. ML model analyzes the data
3. System predicts plant health status
4. Generates detailed PDF report
5. Stores in prediction history

### Key Screens
- **Login/Register**: Secure user authentication
- **Predict**: Input sensor data and get instant predictions
- **History**: View past predictions with download options
- **Admin**: Manage users and all predictions (admin only)

## 🛠️ Tech Stack

### Frontend
- **React 18.3.1** - UI framework
- **React Router 6.28.0** - Client-side routing
- **Axios** - HTTP client
- **CSS3** - Styling

### Backend
- **Python 3.8+** - Programming language
- **Flask 3.1.2** - Web framework
- **scikit-learn** - Machine learning
- **MongoDB** - Database
- **PyMongo** - MongoDB driver
- **ReportLab** - PDF generation
- **Flask-CORS** - Cross-origin support
- **Flask-Limiter** - Rate limiting
- **bcrypt** - Password hashing
- **PyJWT** - JWT authentication

### DevOps & Tools
- **Git** - Version control
- **npm** - Frontend package manager
- **pip** - Python package manager
- **MongoDB** - Database server

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14.0 or higher) and npm
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher)
- **Git**

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShabeehaSarook/AI-Driven-Plant-Health-System.git
cd AI-Driven-Plant-Health-System
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration

# Train the ML model
python scripts/train_model.py

# Run the backend server
python run.py
```

The backend API will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 4. Database Setup

Ensure MongoDB is running:

```bash
# Check MongoDB status
mongosh --eval "db.version()"

# If not running, start MongoDB
# On Windows:
net start MongoDB

# On Linux:
sudo systemctl start mongod

# On Mac:
brew services start mongodb-community
```

## 💻 Usage

### For Users

1. **Register/Login**
   - Create an account or login with existing credentials
   - Receive JWT token for authentication

2. **Make Predictions**
   - Navigate to the Predict page
   - Input 12 environmental parameters:
     - Plant ID
     - Soil Moisture (%)
     - Ambient Temperature (°C)
     - Soil Temperature (°C)
     - Humidity (%)
     - Light Intensity (lux)
     - Soil pH
     - Nitrogen Level (ppm)
     - Phosphorus Level (ppm)
     - Potassium Level (ppm)
     - Chlorophyll Content (SPAD)
     - Electrochemical Signal (V)
   - Click "Predict" to get results
   - Download PDF report

3. **View History**
   - Access all your past predictions
   - Download reports anytime
   - Regenerate reports if needed

### For Admins

1. **Access Admin Dashboard**
   - Login with admin credentials
   - View all user predictions
   - Manage users and data
   - Create/Update/Delete predictions

## 📁 Project Structure

```
AI-Driven-Plant-Health-System/
│
├── backend/                      # Flask Backend API
│   ├── app/                      # Application package
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── utils/               # Utility functions
│   │   └── models/              # Data models
│   ├── config/                  # Configuration
│   ├── data/                    # Training datasets
│   ├── ml_models/               # Trained ML models
│   ├── scripts/                 # Utility scripts
│   ├── reports/                 # Generated PDF reports
│   ├── run.py                   # Entry point
│   ├── requirements.txt         # Python dependencies
│   ├── README.md               # Backend documentation
│   └── API_DOCUMENTATION.md    # API reference
│
├── frontend/                    # React Frontend
│   ├── public/                 # Static files
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   ├── utils/              # Utility functions
│   │   └── App.js              # Main component
│   ├── package.json            # Node dependencies
│   └── .gitignore
│
├── ml-model/                    # Original ML implementation
├── reports/                     # Sample reports
├── .gitignore
└── README.md                   # This file
```

## 📖 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "john_doe"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

### Prediction Endpoints

#### Make Prediction
```http
POST /predict
Authorization: Bearer <token>
Content-Type: application/json

{
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
}
```

#### Get History
```http
GET /history?limit=100
Authorization: Bearer <token>
```

### Admin Endpoints

#### Get All Predictions
```http
GET /admin/predictions
Authorization: Bearer <admin_token>
```

For complete API documentation, see [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)

## 🧠 ML Model Details

### Algorithm
**RandomForest Classifier** - An ensemble learning method that operates by constructing multiple decision trees.

### Features (12 inputs)

| Feature | Type | Range | Unit |
|---------|------|-------|------|
| Plant_ID | Integer | 0-999999 | - |
| Soil_Moisture | Float | 0-100 | % |
| Ambient_Temperature | Float | -50 to 60 | °C |
| Soil_Temperature | Float | -50 to 60 | °C |
| Humidity | Float | 0-100 | % |
| Light_Intensity | Integer | 0-100000 | lux |
| Soil_pH | Float | 0-14 | - |
| Nitrogen_Level | Float | 0-1000 | ppm |
| Phosphorus_Level | Float | 0-1000 | ppm |
| Potassium_Level | Float | 0-1000 | ppm |
| Chlorophyll_Content | Float | 0-100 | SPAD |
| Electrochemical_Signal | Float | -10 to 10 | V |

### Output Classes

- **Healthy**: Plant is in optimal condition
- **Unhealthy**: Plant requires immediate attention
- **At Risk**: Plant shows early warning signs

### Performance Metrics
- Training accuracy and metrics stored in model metadata
- Confidence scores provided with each prediction
- Feature importance analysis available

### Model Training

```bash
cd backend
python scripts/train_model.py
```

This creates:
- `ml_models/plant_model.pkl` - Trained model
- `ml_models/plant_model.meta.json` - Model metadata

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Secure token-based auth
- **Rate Limiting**: Protection against abuse
- **Input Validation**: All inputs sanitized
- **CORS Protection**: Configurable origins
- **Role-Based Access**: User/Admin separation
- **Report Authorization**: Users can only access their own reports

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚢 Deployment

### Backend Deployment (Production)

#### Using Gunicorn
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

#### Environment Variables for Production
```bash
export FLASK_ENV=production
export SECRET_KEY=your-super-secret-production-key
export MONGODB_URI=mongodb://your-production-db
export CORS_ORIGINS=https://yourdomain.com
```

### Frontend Deployment

```bash
cd frontend
npm run build
# Deploy the build/ directory to your hosting service
```

### Docker Support (Coming Soon)
Docker and Docker Compose configurations for easy deployment.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Follow Airbnb style guide
- **Commits**: Use conventional commits

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod
```

### Model Not Found
```bash
# Train the model
cd backend
python scripts/train_model.py
```

### Port Already in Use
```bash
# Backend (Change port in .env)
PORT=5001

# Frontend (Change in package.json)
"start": "PORT=3001 react-scripts start"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Shabeeha Sarook** - [GitHub](https://github.com/ShabeehaSarook)

## 🙏 Acknowledgments

- scikit-learn for ML capabilities
- Flask community for the excellent framework
- React team for the frontend library
- MongoDB for scalable database solution
- ReportLab for PDF generation

## 📧 Contact & Support

- **GitHub Issues**: [Report a bug](https://github.com/ShabeehaSarook/AI-Driven-Plant-Health-System/issues)
- **Email**: shabeehazrook@gmail.com

## 🗺️ Roadmap

- [ ] Docker containerization
- [ ] Real-time sensor integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-plant monitoring
- [ ] Email notifications
- [ ] Weather API integration
- [ ] Plant disease detection with image recognition

---

<p align="center">Made with ❤️ for healthier plants 🌿</p>
