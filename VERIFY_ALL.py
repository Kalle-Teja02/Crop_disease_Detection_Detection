#!/usr/bin/env python
"""
Complete verification that everything is working
Run this before starting the app
"""

import os
import sys
import pickle
import numpy as np
from PIL import Image
from disease_info import disease_data

print("\n" + "="*80)
print("COMPLETE VERIFICATION - CHECKING EVERYTHING")
print("="*80)

# 1. Check model file
print("\n[1/5] Checking model file...")
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
if not os.path.exists(model_path):
    print("  FAILED: Model file not found!")
    sys.exit(1)
size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"  PASSED: Model exists ({size_mb:.2f} MB)")

# 2. Load model
print("\n[2/5] Loading model...")
try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    model = model_data['model']
    scaler = model_data['scaler']
    class_names = model_data['class_names']
    print(f"  PASSED: Model loaded ({len(class_names)} classes)")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

# 3. Check disease data
print("\n[3/5] Checking disease data...")
if len(disease_data) != 16:
    print(f"  FAILED: Expected 16 diseases, got {len(disease_data)}")
    sys.exit(1)
missing = [c for c in class_names if c not in disease_data]
if missing:
    print(f"  FAILED: Missing {len(missing)} classes in disease_data")
    sys.exit(1)
print(f"  PASSED: All 16 diseases in database")

# 4. Test predictions
print("\n[4/5] Testing predictions...")
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
        print(f"  FAILED: No images in {folder}")
        all_correct = False
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.flatten().reshape(1, -1)
    
    img_scaled = scaler.transform(img_array)
    predictions = model.predict_proba(img_scaled)[0]
    prediction_idx = np.argmax(predictions)
    predicted_class = class_names[int(prediction_idx)]
    
    is_correct = crop_name in predicted_class
    if not is_correct:
        print(f"  FAILED: {crop_name} predicted as {predicted_class}")
        all_correct = False

if all_correct:
    print(f"  PASSED: All 5 crops predict correctly")
else:
    print(f"  FAILED: Some predictions are wrong")
    sys.exit(1)

# 5. Check app.py
print("\n[5/5] Checking app.py...")
app_path = os.path.join(os.path.dirname(__file__), 'app.py')
if not os.path.exists(app_path):
    print("  FAILED: app.py not found")
    sys.exit(1)
print(f"  PASSED: app.py exists")

# Final summary
print("\n" + "="*80)
print("ALL CHECKS PASSED!")
print("="*80)
print("\nYou can now start the app with:")
print("  python crop-disease-detection/app.py")
print("\nThen open: http://localhost:5000")
print("="*80 + "\n")
