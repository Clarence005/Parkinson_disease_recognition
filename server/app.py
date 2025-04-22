import torch
from PIL import Image
from torchvision import transforms
from transformers import SwinForImageClassification, SwinConfig, AutoImageProcessor
from flask import Flask, request, jsonify
import os

# === CONFIG ===
MODEL_NAME = "microsoft/swin-tiny-patch4-window7-224"
MODEL_PATH = "best_swin_model.pt" 
NUM_CLASSES = 2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = 224
CLASS_NAMES = ["healthy", "patient"]  


app = Flask(__name__)

# === LOAD MODEL ===
print("Loading model...")
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
normalize = transforms.Normalize(mean=image_processor.image_mean, std=image_processor.image_std)

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    normalize,
])

def load_model():
    config = SwinConfig.from_pretrained(MODEL_NAME)
    config.num_labels = NUM_CLASSES
    model = SwinForImageClassification.from_pretrained(
        MODEL_NAME, config=config, ignore_mismatched_sizes=True
    )
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

model = load_model()

# === API ENDPOINT ===
@app.route('/predict', methods=['POST'])
def predict():
    print("Mobile connected...")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image = Image.open(file.stream).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(pixel_values=image_tensor)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            pred_class = torch.argmax(probs, dim=1).item()

        result = {
            "class_name": CLASS_NAMES[pred_class],
            "confidence": float(probs[0][pred_class])
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
