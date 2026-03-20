"""
Debug script to test the app's prediction logic
Run this to see exactly what the app is doing
"""

import os
import sys
import pickle
import numpy as np
from PIL import Image
from disease_info import disease_data

print("\n" + "="*80)
print("APP DEBUGGING - CHECKING EVERYTHING")
print("="*80)

# 1. Check model file
print("\n1. MODEL FILE CHECK:")
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   Model exists: {model_path}")
    print(f"   Size: {size_mb:.2f} MB")
else:
    print(f"   ERROR: Model not found!")
    sys.exit(1)

# 2. Load model
print("\n2. LOADING MODEL:")
try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    scaler = model_data['scaler']
    class_names = model_data['class_names']
    
    print(f"   Model loaded successfully")
    print(f"   Classes: {len(class_names)}")
    print(f"   Model type: {type(model).__name__}")
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# 3. Check disease_data
print("\n3. DISEASE DATA CHECK:")
print(f"   Total diseases: {len(disease_data)}")
missing = [c for c in class_names if c not in disease_data]
if missing:
    print(f"   ERROR: Missing {len(missing)} classes!")
    for m in missing:
        print(f"      - {m}")
    sys.exit(1)
else:
    print(f"   All {len(class_names)} classes found in disease_data")

# 4. Test predictions
print("\n4. TESTING PREDICTIONS:")
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_cases = [
    ('Corn___healthy', 'Corn'),
    ('Grape___healthy', 'Grape'),
    ('Pepper___healthy', 'Pepper'),
    ('Potato___healthy', 'Potato'),
    ('Tomato___healthy', 'Tomato'),
]

all_correct = True

for folder, crop_name in test_cases:
    folder_path = os.path.join(dataset_path, folder)
    
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"   {crop_name}: NO IMAGES")
        all_correct = False
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    # Load and preprocess
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.flatten().reshape(1, -1)
    
    img_scaled = scaler.transform(img_array)
    
    predictions = model.predict_proba(img_scaled)[0]
    prediction_idx = np.argmax(predictions)
    confidence = predictions[prediction_idx] * 100
    
    predicted_class = class_names[int(prediction_idx)]
    disease_info = disease_data.get(predicted_class, {})
    disease_name = disease_info.get('name', predicted_class)
    
    is_correct = crop_name in predicted_class
    
    status = "PASS" if is_correct else "FAIL"
    print(f"   {crop_name}: {status}")
    print(f"      Predicted: {predicted_class}")
    print(f"      Disease: {disease_name}")
    print(f"      Confidence: {confidence:.2f}%")
    
    if not is_correct:
        all_correct = False

print("\n" + "="*80)
if all_correct:
    print("SUCCESS: All predictions are correct!")
    print("If the app is still showing wrong diseases, the issue is:")
    print("  1. Flask app is not restarted (old code in memory)")
    print("  2. You're uploading images from wrong crops")
    print("  3. Browser cache issue")
else:
    print("ERROR: Model predictions are wrong!")
    print("Need to retrain the model")

print("="*80 + "\n")
