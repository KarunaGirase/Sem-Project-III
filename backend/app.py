from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Base directories
BASE = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE, "models")

# Load trained models and preprocessors
crop_clf = joblib.load(os.path.join(MODELS_DIR, "crop_clf.pkl"))
yield_reg = joblib.load(os.path.join(MODELS_DIR, "yield_reg.pkl"))
fert_clf = joblib.load(os.path.join(MODELS_DIR, "fert_clf.pkl"))
fert_qty_reg = joblib.load(os.path.join(MODELS_DIR, "fert_qty_reg.pkl"))
le_crop = joblib.load(os.path.join(MODELS_DIR, "le_crop.pkl"))
le_fert = joblib.load(os.path.join(MODELS_DIR, "le_fert.pkl"))
preproc = joblib.load(os.path.join(MODELS_DIR, "preprocessor.pkl"))

# Import prediction function
from predict import make_prediction


# ✅ Home route (prevents 404 Not Found)
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🌾 Crop Management System API is running successfully!",
        "endpoints": ["/predict"]
    })


# ✅ Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Use helper function from predict.py
        result = make_prediction(data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
