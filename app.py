from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app)

MODEL_PATH = "waste_sorting_model.h5"
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

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image uploaded"
        }), 400

    try:
        file = request.files["image"]
        image_bytes = file.read()

        processed_image = preprocess_image(image_bytes)

        predictions = model.predict(processed_image, verbose=0)[0]

        class_id = int(np.argmax(predictions))
        confidence = float(predictions[class_id])

        predicted_class = CLASS_NAMES[class_id]

        print("\n==========================")
        print("Predictions:", predictions)
        print("Class ID:", class_id)
        print("Class Name:", predicted_class)
        print("Confidence:", confidence)
        print("==========================\n")

        if confidence < CONFIDENCE_THRESHOLD:
            return jsonify({
                "success": True,
                "class_name": "unknown",
                "confidence": confidence
            })

        return jsonify({
            "success": True,
            "class_name": predicted_class,
            "confidence": confidence
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return "Waste Sorting API Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)