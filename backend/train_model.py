import os
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

# --- Paths ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "CropDatasetFinal.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# --- Load dataset ---
df = pd.read_csv(DATA_PATH)
print(f"✅ Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")

# --- Encode categorical features ---
cat_cols = ['Villages', 'Soil_Type', 'Crop_Season']
target_cols = ['Crop_Name', 'Fertilizer_Type']

label_encoders = {}
for col in cat_cols + target_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# --- Prepare features and targets ---
X = df[['Year', 'Avg_Temp_C', 'Avg_Humidity_Percent', 'Soil_pH',
        'Soil_N_kg_ha', 'Soil_P_kg_ha', 'Soil_K_kg_ha',
        'Rainfall_mm', 'Farm_Area_ha'] + cat_cols].copy()   # copy to avoid view problems

y_crop = df['Crop_Name']
y_yield = df['Yield_kg_ha']
y_fert_type = df['Fertilizer_Type']
y_fert_qty = df['Fertilizer_Quantity_kg_ha']

# --- Scale numeric columns ---
num_cols = ['Year', 'Avg_Temp_C', 'Avg_Humidity_Percent', 'Soil_pH',
            'Soil_N_kg_ha', 'Soil_P_kg_ha', 'Soil_K_kg_ha',
            'Rainfall_mm', 'Farm_Area_ha']
scaler = StandardScaler()
X.loc[:, num_cols] = scaler.fit_transform(X[num_cols])

# --- Split data ---
X_train, X_test, yc_train, yc_test, yy_train, yy_test, yft_train, yft_test, yfq_train, yfq_test = train_test_split(
    X, y_crop, y_yield, y_fert_type, y_fert_qty, test_size=0.2, random_state=42
)

# --- Train models ---
print("\n🧠 Training models...")

crop_clf = RandomForestClassifier(n_estimators=200, random_state=42)
crop_clf.fit(X_train, yc_train)
crop_acc = accuracy_score(yc_test, crop_clf.predict(X_test))
print("🌾 Crop model accuracy:", crop_acc)

yield_reg = RandomForestRegressor(n_estimators=200, random_state=42)
yield_reg.fit(X_train, yy_train)
yy_pred = yield_reg.predict(X_test)
yield_rmse = float(np.sqrt(mean_squared_error(yy_test, yy_pred)))
yield_r2 = float(r2_score(yy_test, yy_pred))
print(f"📈 Yield RMSE: {yield_rmse:.4f}, R2: {yield_r2:.4f}")

fert_clf = RandomForestClassifier(n_estimators=200, random_state=42)
fert_clf.fit(X_train, yft_train)
fert_acc = accuracy_score(yft_test, fert_clf.predict(X_test))
print("💧 Fertilizer type accuracy:", fert_acc)

fert_qty_reg = RandomForestRegressor(n_estimators=200, random_state=42)
fert_qty_reg.fit(X_train, yfq_train)
q_pred = fert_qty_reg.predict(X_test)
fert_qty_rmse = float(np.sqrt(mean_squared_error(yfq_test, q_pred)))
fert_qty_r2 = float(r2_score(yfq_test, q_pred))
print(f"⚖️ Fertilizer quantity RMSE: {fert_qty_rmse:.4f}, R2: {fert_qty_r2:.4f}")

# --- Save models ---
print("\n💾 Saving new models...")
joblib.dump(crop_clf, os.path.join(MODELS_DIR, "crop_clf.pkl"))
joblib.dump(yield_reg, os.path.join(MODELS_DIR, "yield_reg.pkl"))
joblib.dump(fert_clf, os.path.join(MODELS_DIR, "fert_clf.pkl"))
joblib.dump(fert_qty_reg, os.path.join(MODELS_DIR, "fert_qty_reg.pkl"))
joblib.dump(label_encoders['Crop_Name'], os.path.join(MODELS_DIR, "le_crop.pkl"))
joblib.dump(label_encoders['Fertilizer_Type'], os.path.join(MODELS_DIR, "le_fert.pkl"))

preproc = {
    'label_encoders': {col: label_encoders[col] for col in cat_cols},
    'scaler': scaler,
    'numeric_columns': num_cols,
    'X_columns': X.columns.tolist()
}
joblib.dump(preproc, os.path.join(MODELS_DIR, "preprocessor.pkl"))

print("\n✅ Training complete. Models saved in:", MODELS_DIR)
