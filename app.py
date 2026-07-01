from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = "waste_sorting_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = {
    0: "fruit_peel",
    1: "not_peels",
    2: "vegetable_peel"
}
CONFIDENCE_THRESHOLD = 0.50


def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img).astype("float32")
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


@app.route("/predict", methods=["POST"])
def predict():
    requested_type = request.form.get("type") 

    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    try:
        file = request.files["image"]
        image_bytes = file.read()
        processed_image = preprocess_image(image_bytes)
        
        predictions = model.predict(processed_image, verbose=0)[0]
        class_id = int(np.argmax(predictions))
        confidence = float(predictions[class_id])
        predicted_class = CLASS_NAMES[class_id]

        if predicted_class == "not_peels":
            return jsonify({
                "success": False,
                "error": "The image was rejected. The AI classified it as: not peels."
            }), 400

        is_valid = False
        if requested_type == 'veg' and predicted_class == 'vegetable_peel':
            is_valid = True
        elif requested_type == 'fruit' and predicted_class == 'fruit_peel':
            is_valid = True

        if not is_valid or confidence < CONFIDENCE_THRESHOLD:
            return jsonify({
                "success": False, 
                "error": f"The image was rejected. The AI classified it as: {predicted_class.replace('_', ' ')}."
            }), 400

        return jsonify({"success": True, "class_name": predicted_class, "confidence": confidence})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/")
def home():
    return "Waste Sorting API Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)