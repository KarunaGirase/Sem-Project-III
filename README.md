
# Crop Management System - Complete Project (Generated)

This project contains a Flask backend, a Bootstrap frontend, dataset, and trained ML models (RandomForest baseline).
You can open this folder in VS Code and run locally.

## Structure
/mnt/data/CropManagementSystem

## Quick start
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   cd backend
   python app.py
   ```
4. Open `frontend/index.html` in the browser (or use Live Server extension in VS Code).
5. Fill form and click Predict (backend must be running).

## Models & Metrics (trained during packaging)
- Crop accuracy: 0.5938
- Yield RMSE: 10750.17, R2: 0.4584
- Fertilizer type accuracy: 0.8234
- Fertilizer quantity RMSE: 74.15, R2: 0.4873

## Notes
- The frontend sends data to `http://127.0.0.1:5000/predict`.
- If you want to retrain models, use `backend/train_model.py` (provided minimal script) or adapt the training block in this package.
