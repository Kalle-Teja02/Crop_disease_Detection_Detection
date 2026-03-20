"""
Simulate exactly what the Flask app does
This will help us understand what's going wrong
"""

import os
import sys
import pickle
import numpy as np
from PIL import Image as PILImage
from disease_info import disease_data

print("\n" + "="*80)
print("SIMULATING FLASK APP BEHAVIOR")
print("="*80)

# Step 1: Load model (exactly like app.py does)
print("\n[STEP 1] Loading model...")

app_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(app_dir)

possible_paths = [
    os.path.join(app_dir, 'model_cnn.pkl'),
    os.path.join(parent_dir, 'model_cnn.pkl'),
    os.path.join(parent_dir, 'crop-disease-detection', 'model_cnn.pkl'),
]

model_path = None
for path in possible_paths:
    if os.path.exists(path):
        model_path = path
        print(f"  Found model at: {path}")
        break

if not model_path:
    print(f"  ERROR: Model not found in any location!")
    sys.exit(1)

try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    scaler = model_data['scaler']
    class_names = model_data['class_names']
    
    print(f"  Model loaded successfully")
    print(f"  Classes: {len(class_names)}")
    print(f"  Model type: {type(model).__name__}")
    USE_MODEL = True
except Exception as e:
    print(f"  ERROR: {e}")
    USE_MODEL = False
    sys.exit(1)

# Step 2: Test with each crop
print("\n[STEP 2] Testing predictions...")

dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_cases = [
    ('Corn___healthy', 'Corn'),
    ('Grape___healthy', 'Grape'),
    ('Pepper___healthy', 'Pepper'),
    ('Potato___healthy', 'Potato'),
    ('Tomato___healthy', 'Tomato'),
]

for folder, crop_name in test_cases:
    folder_path = os.path.join(dataset_path, folder)
    
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"\n{crop_name}: NO IMAGES")
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    print(f"\n{crop_name}:")
    print(f"  Image: {img_file}")
    
    # EXACT app.py logic
    try:
        img = PILImage.open(img_path).convert('RGB')
        img = img.resize((64, 64))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = img_array.flatten().reshape(1, -1)
        
        img_scaled = scaler.transform(img_array)
        
        predictions = model.predict_proba(img_scaled)[0]
        prediction_idx = np.argmax(predictions)
        confidence = predictions[prediction_idx] * 100
        
        predicted_class = class_names[int(prediction_idx)]
        
        # Get disease info (EXACT app.py logic)
        disease_info = disease_data.get(predicted_class, {
            'name': predicted_class.replace('___', ' - ').replace('_', ' '),
            'symptoms': 'Information not available',
            'treatment': 'Consult agricultural expert'
        })
        
        disease_name = disease_info['name']
        
        print(f"  Predicted class: {predicted_class}")
        print(f"  Disease name: {disease_name}")
        print(f"  Confidence: {confidence:.2f}%")
        
        # Check if correct
        is_correct = crop_name in predicted_class
        print(f"  Correct: {'YES' if is_correct else 'NO'}")
        
        if not is_correct:
            print(f"  ERROR: Expected {crop_name}, got {predicted_class}")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
