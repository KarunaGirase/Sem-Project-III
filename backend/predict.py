import os
import pandas as pd
import numpy as np
import joblib

# --- Load pre-trained models and preprocessing objects ---
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")

crop_clf = joblib.load(os.path.join(MODELS_DIR, "crop_clf.pkl"))
yield_reg = joblib.load(os.path.join(MODELS_DIR, "yield_reg.pkl"))
fert_clf = joblib.load(os.path.join(MODELS_DIR, "fert_clf.pkl"))
fert_qty_reg = joblib.load(os.path.join(MODELS_DIR, "fert_qty_reg.pkl"))
preproc = joblib.load(os.path.join(MODELS_DIR, "preprocessor.pkl"))
le_crop = joblib.load(os.path.join(MODELS_DIR, "le_crop.pkl"))
le_fert = joblib.load(os.path.join(MODELS_DIR, "le_fert.pkl"))

def make_prediction(data: dict):
    """
    Expects a dictionary of input data from frontend form.
    """

    df2 = pd.DataFrame([data])

    # --- Encode categorical columns same as training ---
    for col, le in preproc['label_encoders'].items():
        if col in df2.columns:
            val = df2.at[0, col]
            # Handle unseen categories gracefully
            if val not in le.classes_:
                # add new class dynamically to avoid KeyError
                le.classes_ = np.append(le.classes_, val)
            df2.at[0, col] = le.transform([val])[0]

    # --- Scale numeric features ---
    nums = preproc['numeric_columns']
    df2[nums] = preproc['scaler'].transform(df2[nums])

    # --- Ensure correct column order ---
    X = df2[preproc['X_columns']]

    # --- Make predictions ---
    crop_pred = crop_clf.predict(X)[0]
    yield_pred = yield_reg.predict(X)[0]
    fert_type_pred = fert_clf.predict(X)[0]
    fert_qty_pred = fert_qty_reg.predict(X)[0]

    # --- Decode categorical predictions ---
    crop_name = le_crop.inverse_transform([int(crop_pred)])[0]
    fert_type = le_fert.inverse_transform([int(fert_type_pred)])[0]

    result = {
        "Predicted Crop": crop_name,
        "Predicted Yield (kg/ha)": round(float(yield_pred), 2),
        "Recommended Fertilizer": fert_type,
        "Fertilizer Quantity (kg/ha)": round(float(fert_qty_pred), 2),
    }

    return result
