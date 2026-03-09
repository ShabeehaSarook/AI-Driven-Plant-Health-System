# API Documentation

## Base URL

```
http://localhost:5000
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Health Check

**GET /** 

Check if the API is running.

**Response:**
```json
{
  "message": "Smart Plant Health Monitoring API",
  "status": "running",
  "version": "1.0.0"
}
```

---

### 2. User Registration

**POST /register**

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "username": "johndoe"
}
```

**Validation Rules:**
- Email: Valid email format, max 254 characters
- Password: 8-128 characters
- Username: Optional, 1-100 characters

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Rate Limit:** 5 requests per minute

---

### 3. User Login

**POST /login**

Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "username": "johndoe",
    "role": "user"
  }
}
```

**Rate Limit:** 10 requests per minute

---

### 4. Make Prediction

**POST /predict** 🔒

Make a plant health prediction.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
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

**Field Ranges:**
- Plant_ID: 0-999999
- Soil_Moisture: 0-100 (%)
- Ambient_Temperature: -50 to 60 (°C)
- Soil_Temperature: -50 to 60 (°C)
- Humidity: 0-100 (%)
- Light_Intensity: 0-100000 (lux)
- Soil_pH: 0-14
- Nitrogen_Level: 0-1000 (ppm)
- Phosphorus_Level: 0-1000 (ppm)
- Potassium_Level: 0-1000 (ppm)
- Chlorophyll_Content: 0-100 (SPAD)
- Electrochemical_Signal: -10 to 10 (V)

**Response (200):**
```json
{
  "prediction": "Healthy",
  "confidence": "95.67%",
  "confidence_percent": 95.67,
  "model_version": "2024-01-15T10:30:00Z",
  "explanation": {
    "top_factors": [
      {
        "feature": "Soil_Moisture",
        "importance": 0.156,
        "value": 45.5
      },
      {
        "feature": "Chlorophyll_Content",
        "importance": 0.142,
        "value": 45.8
      }
    ]
  },
  "plant_message": "Your plant is thriving! Keep up the great care.",
  "report": "/reports/plant_health_report_20240115_103045_123456.pdf"
}
```

---

### 5. Get Prediction History

**GET /history** 🔒

Get prediction history for the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 100, max: 1000)

**Example:**
```
GET /history?limit=50
```

**Response (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "user_id": "507f191e810c19729de860ea",
    "prediction": "Healthy",
    "confidence": "95.67%",
    "confidence_percent": 95.67,
    "timestamp": "2024-01-15T10:30:45Z",
    "report": "/reports/plant_health_report_20240115_103045_123456.pdf",
    "input": {
      "Plant_ID": 1,
      "Soil_Moisture": 45.5
      // ... other features
    }
  }
]
```

---

### 6. Regenerate Report

**POST /predictions/:prediction_id/report/regenerate** 🔒

Regenerate a PDF report for an existing prediction.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Report regenerated",
  "report": "/reports/plant_health_report_20240115_140530_654321.pdf"
}
```

---

### 7. Download Report

**GET /reports/:filename** 🔒

Download a PDF report.

**Headers:**
```
Authorization: Bearer <token>
```

**Example:**
```
GET /reports/plant_health_report_20240115_103045_123456.pdf
```

**Response:** PDF file download

**Authorization:** Users can only download their own reports.

---

## Admin Endpoints 👑

All admin endpoints require an admin role.

### 8. Get All Predictions

**GET /admin/predictions** 🔒👑

Get all predictions (admin only).

**Query Parameters:**
- `limit` (optional): Number of records (default: 100)

**Response (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "user_id": "507f191e810c19729de860ea",
    "prediction": "Healthy",
    "confidence_percent": 95.67,
    "timestamp": "2024-01-15T10:30:45Z"
  }
]
```

---

### 9. Create Prediction (Admin)

**POST /admin/predictions** 🔒👑

Manually create a prediction record.

**Request Body:**
```json
{
  "user_id": "507f191e810c19729de860ea",
  "prediction": "Healthy",
  "confidence_percent": 95.5,
  "input": {
    "Plant_ID": 1,
    "Soil_Moisture": 45.5
    // ... other features
  }
}
```

---

### 10. Update Prediction

**PUT /admin/predictions/:id** 🔒👑

Update an existing prediction.

**Request Body:**
```json
{
  "prediction": "At Risk",
  "confidence_percent": 87.3
}
```

---

### 11. Delete Prediction

**DELETE /admin/predictions/:id** 🔒👑

Delete a prediction and its associated report.

**Response (200):**
```json
{
  "message": "Prediction deleted"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "code": "error_code",
  "details": {
    // Optional additional details
  }
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `validation_error` | 400 | Invalid input data |
| `unauthorized` | 401 | Missing or invalid token |
| `forbidden` | 403 | Insufficient permissions |
| `not_found` | 404 | Resource not found |
| `rate_limited` | 429 | Too many requests |
| `internal_error` | 500 | Server error |

### Examples

**Validation Error (400):**
```json
{
  "error": "Invalid input",
  "code": "validation_error",
  "details": {
    "fields": {
      "Soil_Moisture": "Must be between 0 and 100"
    }
  }
}
```

**Unauthorized (401):**
```json
{
  "error": "Token is missing",
  "code": "unauthorized"
}
```

**Forbidden (403):**
```json
{
  "error": "Admin access required",
  "code": "forbidden"
}
```

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/register` | 5 per minute |
| `/login` | 10 per minute |
| All others | 200 per day, 50 per hour |

When rate limited, you'll receive a 429 status code.

---

## Best Practices

1. **Store tokens securely** - Never expose JWT tokens in URLs or logs
2. **Refresh tokens** - Implement token refresh before expiration
3. **Validate input** - Always validate data on the client side too
4. **Handle errors** - Implement proper error handling for all requests
5. **Use HTTPS** - Always use HTTPS in production

---

## Postman Collection

Import this into Postman for easy testing:

```json
{
  "info": {
    "name": "Plant Health API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000"
    },
    {
      "key": "token",
      "value": ""
    }
  ]
}
```
