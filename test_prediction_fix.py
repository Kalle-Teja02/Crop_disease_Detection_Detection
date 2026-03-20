"""
Quick test to verify the prediction fix works correctly
"""

import os
import pickle
import numpy as np
from PIL import Image

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')

if not os.path.exists(model_path):
    print(f"ERROR: Model not found at {model_path}")
    print("Please run train_cnn_model.py first")
    exit(1)

with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
scaler = model_data['scaler']
class_names = model_data['class_names']

print("\n" + "="*80)
print("TESTING PREDICTION FIX")
print("="*80)
print(f"\nModel loaded successfully")
print(f"Classes: {len(class_names)}")
print(f"Scaler input shape: {scaler.n_features_in_}")

# Test the FIXED prediction method (same as app.py update)
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_crops = ['Corn___healthy', 'Potato___healthy', 'Tomato___healthy']

print(f"\nTesting with sample images from each crop:\n")

for test_class in test_crops:
    folder_path = os.path.join(dataset_path, test_class)
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue
    
    # Get first original image
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"No images in {test_class}")
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    # FIXED METHOD: Same as updated app.py
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))  # 64x64 (NOT 128x128)
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    # Flatten and reshape
    img_flat = img_array.flatten().reshape(1, -1)
    
    # Scale using scaler
    features_scaled = scaler.transform(img_flat)
    
    # Get prediction
    predictions = model.predict_proba(features_scaled)[0]
    predicted_idx = np.argmax(predictions)
    confidence = predictions[predicted_idx] * 100
    predicted_class = class_names[predicted_idx]
    
    # Check if correct
    expected_crop = test_class.split('___')[0]
    predicted_crop = predicted_class.split('___')[0]
    is_correct = expected_crop == predicted_crop
    
    status = "✅ CORRECT" if is_correct else "❌ WRONG"
    
    print(f"Test: {test_class}")
    print(f"  Predicted: {predicted_class}")
    print(f"  Confidence: {confidence:.2f}%")
    print(f"  {status}")
    print()

print("="*80)
print("Test complete! The prediction fix should now work correctly.")
print("="*80)
