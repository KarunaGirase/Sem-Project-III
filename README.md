# 🌾 Crop Management System

## 📌 Project Overview

The Crop Management System is an AI-powered agricultural decision support system that helps farmers and agricultural professionals make data-driven decisions.

Using Machine Learning models, the system provides:

* 🌱 Crop Recommendation
* 📈 Yield Prediction
* 🧪 Fertilizer Recommendation
* 📊 Fertilizer Quantity Estimation

The system uses environmental and soil parameters to generate accurate predictions and recommendations.

---

## 🚀 Features

### 🌱 Crop Prediction

Predicts the most suitable crop based on agricultural conditions.

### 📈 Yield Estimation

Estimates expected crop yield using machine learning regression models.

### 🧪 Fertilizer Recommendation

Recommends the best fertilizer type for the selected field conditions.

### ⚖️ Fertilizer Quantity Prediction

Predicts the required fertilizer quantity for optimal crop growth.

### 🌐 User-Friendly Interface

Interactive web interface built using HTML, CSS, Bootstrap, and JavaScript.

### 🔗 REST API

Flask-based backend API for prediction services.

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Machine Learning

* Scikit-Learn
* Random Forest
* Regression Models
* Label Encoding
* Data Preprocessing Pipelines

### Data Handling

* Pandas
* NumPy

### Model Serialization

* Joblib

---

## 📂 Project Structure

```text
CropManagementSystem/
│
├── backend/
│   ├── app.py
│   ├── predict.py
│   ├── train_model.py
│   ├── utils.py
│   └── models/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   ├── CropDatasetFinal.csv
│   └── crop_data.csv
│
├── src/
│   ├── crop_prediction.py
│   ├── fertilizer_recommendation.py
│   └── rainfall_yield.py
│
├── requirements.txt
└── README.md
```

---

## 📊 Machine Learning Modules

### Crop Recommendation Model

Predicts the most suitable crop using environmental and soil parameters.

### Yield Prediction Model

Estimates crop production using regression techniques.

### Fertilizer Recommendation Model

Suggests the most effective fertilizer based on crop and soil characteristics.

### Fertilizer Quantity Model

Calculates the recommended amount of fertilizer required.

---

## 📥 Installation

### Clone Repository

```bash
git clone <repository-url>
cd CropManagementSystem
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start Backend

```bash
cd backend
python app.py
```

Backend runs at:

```text
http://127.0.0.1:5000
```

### Open Frontend

Open:

```text
frontend/index.html
```

or use VS Code Live Server.

---

## 🔌 API Endpoints

### Home

```http
GET /
```

Response:

```json
{
  "message": "Crop Management System API is running successfully!"
}
```

### Prediction

```http
POST /predict
```

Returns:

* Recommended Crop
* Estimated Yield
* Fertilizer Type
* Fertilizer Quantity

---

## 📈 Future Enhancements

* Weather API Integration
* Real-Time Soil Analysis
* Mobile Application
* Multi-language Support
* Advanced Deep Learning Models
* Cloud Deployment

---

## 🎯 Applications

* Smart Agriculture
* Precision Farming
* Agricultural Research
* Crop Planning
* Farm Management Systems

---

## 👩‍💻 Author

Karuna Girase

B.Tech (Data Science)

Machine Learning | Data Science | AI Enthusiast

```
```
