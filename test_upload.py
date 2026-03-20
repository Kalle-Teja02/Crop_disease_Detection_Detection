"""
Test what happens when we upload an image through the app
This simulates the exact Flask predict() function
"""

import os
import sys
import pickle
import numpy as np
from PIL import Image
from disease_info import disease_data

print("\n" + "="*80)
print("TESTING EXACT APP UPLOAD FLOW")
print("="*80)

# Load model exactly like app.py does
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
print(f"\n1. Loading model from: {model_path}")
print(f"   File exists: {os.path.exists(model_path)}")

try:
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    scaler = model_data['scaler']
    class_names = model_data['class_names']
    
    print(f"   Model loaded: YES")
    print(f"   Classes: {len(class_names)}")
    print(f"   Classes: {class_names}")
except Exception as e:
    print(f"   ERROR loading model: {e}")
    sys.exit(1)

# Test with each crop
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_cases = [
    ('Corn___healthy', 'Corn'),
    ('Grape___healthy', 'Grape'),
    ('Pepper___healthy', 'Pepper'),
    ('Potato___healthy', 'Potato'),
    ('Tomato___healthy', 'Tomato'),
]

print("\n2. Testing predictions:\n")

for folder, crop_name in test_cases:
    folder_path = os.path.join(dataset_path, folder)
    
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"{crop_name}: NO IMAGES FOUND")
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    print(f"{crop_name} Test:")
    print(f"  Image: {img_file}")
    print(f"  Path: {img_path}")
    print(f"  Exists: {os.path.exists(img_path)}")
    
    try:
        # EXACT app.py logic
        img = Image.open(img_path).convert('RGB')
        img = img.resize((64, 64))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = img_array.flatten().reshape(1, -1)
        
        print(f"  Image shape: {img_array.shape}")
        
        img_scaled = scaler.transform(img_array)
        print(f"  Scaled shape: {img_scaled.shape}")
        
        predictions = model.predict_proba(img_scaled)[0]
        print(f"  Predictions shape: {predictions.shape}")
        print(f"  Predictions sum: {predictions.sum():.4f}")
        
        prediction_idx = np.argmax(predictions)
        confidence = predictions[prediction_idx] * 100
        
        predicted_class = class_names[int(prediction_idx)]
        
        print(f"  Predicted class: {predicted_class}")
        print(f"  Confidence: {confidence:.2f}%")
        
        # Get disease info
        disease_info = disease_data.get(predicted_class, {
            'name': predicted_class.replace('___', ' - ').replace('_', ' '),
            'symptoms': 'Information not available',
            'treatment': 'Consult agricultural expert'
        })
        
        disease_name = disease_info['name']
        print(f"  Disease name: {disease_name}")
        
        # Check if correct
        is_correct = crop_name in predicted_class
        print(f"  Correct: {'YES' if is_correct else 'NO'}")
        
        # Show top 3
        top_3_indices = np.argsort(predictions)[-3:][::-1]
        print(f"  Top 3 predictions:")
        for i, idx in enumerate(top_3_indices):
            print(f"    {i+1}. {class_names[idx]}: {predictions[idx]*100:.2f}%")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()

print("="*80)
