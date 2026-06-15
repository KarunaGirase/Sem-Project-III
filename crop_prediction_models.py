#!/usr/bin/env python3
"""
crop_prediction_models.py

Train Random Forest, Decision Tree, and SVM (RBF) to predict Crop using crop_data.csv.
Uses cross-validation to reduce overfitting risk and prints metrics.
Saves trained models as joblib files.

Usage:
    python crop_prediction_models.py
"""
import os
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), "crop_data.csv")

def load_and_prepare():
    df = pd.read_csv(DATA_PATH)
    if 'Crop' not in df.columns:
        raise RuntimeError("crop_data.csv must contain a 'Crop' column.")
    df = df.dropna(subset=['Crop'])
    # canonicalize crop names
    df['Crop_clean'] = df['Crop'].astype(str).str.strip().str.lower()
    def canon_crop(name):
        if 'rice' in name: return 'rice'
        if 'wheat' in name: return 'wheat'
        if 'maize' in name or 'corn' in name: return 'maize'
        return name
    df['Crop_final'] = df['Crop_clean'].apply(canon_crop)
    # features
    expected = ['Temperature','Humidity','Soil_Type','Rainfall']
    for c in expected:
        if c not in df.columns:
            raise RuntimeError(f"Expected feature column '{c}' in dataset.")
    X = df[expected].copy()
    for col in X.select_dtypes(include=['object','category']).columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))
    y = df['Crop_final'].astype(str)
    le_y = LabelEncoder().fit(y)
    y_enc = le_y.transform(y)
    return X, y_enc, le_y

def train_models(X, y_enc, le_y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=test_size, random_state=random_state, stratify=y_enc)

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=12, min_samples_leaf=5,
            class_weight='balanced', random_state=random_state),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=12, min_samples_leaf=5, class_weight='balanced', random_state=random_state),
        "SVM (scaled rbf)": make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=False, random_state=random_state))
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    for name, model in models.items():
        # Cross-validation accuracy
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred, target_names=list(le_y.classes_), zero_division=0)
        results[name] = {
            'model': model, 'accuracy': acc, 'cv_mean': np.mean(cv_scores),
            'confusion_matrix': cm, 'report': cr, 'y_test': y_test, 'y_pred': y_pred
        }
        joblib.dump(model, os.path.join(os.path.dirname(__file__), f"{name.replace(' ', '_')}_crop_model.joblib"))
    return results

def pretty_print(results, le_y):
    for name, r in results.items():
        print("\n" + "="*70)
        print(f"Model: {name}")
        print(f"Accuracy on test set: {r['accuracy']*100:.2f}%")
        print(f"Mean CV accuracy: {r['cv_mean']*100:.2f}%")
        print("Confusion Matrix (rows=true classes, cols=predicted classes):")
        df_cm = pd.DataFrame(r['confusion_matrix'], index=le_y.classes_, columns=le_y.classes_)
        print(df_cm)
        print("\nClassification report:")
        print(r['report'])
        print("\nConfusion-matrix elements (as flat list row-wise):", r['confusion_matrix'].ravel().tolist())
    best = max(results.keys(), key=lambda k: results[k]['accuracy'])
    print("\n" + "="*70)
    print(f"BEST MODEL: {best} — {results[best]['accuracy']*100:.2f}%")

if __name__ == "__main__":
    X, y_enc, le_y = load_and_prepare()
    results = train_models(X, y_enc, le_y)
    pretty_print(results, le_y)
