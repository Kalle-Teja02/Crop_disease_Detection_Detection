"""
Show what the model predicts for each crop
This helps verify the model is working correctly
"""

import os
import pickle
import numpy as np
from PIL import Image
from disease_info import disease_data

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
scaler = model_data['scaler']
class_names = model_data['class_names']

dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

print("\n" + "="*80)
print("MODEL PREDICTIONS FOR EACH CROP")
print("="*80)

crops = ['Corn', 'Grape', 'Pepper', 'Potato', 'Tomato']

for crop in crops:
    print(f"\n{crop.upper()}:")
    print("-" * 80)
    
    # Find all classes for this crop
    crop_classes = [c for c in class_names if crop in c]
    
    for class_name in crop_classes:
        folder_path = os.path.join(dataset_path, class_name)
        
        # Get first image
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                      and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
        
        if not image_files:
            continue
        
        img_file = image_files[0]
        img_path = os.path.join(folder_path, img_file)
        
        # Load and predict
        img = Image.open(img_path).convert('RGB')
        img = img.resize((64, 64))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = img_array.flatten().reshape(1, -1)
        
        img_scaled = scaler.transform(img_array)
        predictions = model.predict_proba(img_scaled)[0]
        predicted_idx = np.argmax(predictions)
        predicted_class = class_names[predicted_idx]
        confidence = predictions[predicted_idx] * 100
        
        # Get disease name
        disease_info = disease_data.get(predicted_class, {})
        disease_name = disease_info.get('name', predicted_class)
        
        # Check if correct
        is_correct = crop in predicted_class
        status = "OK" if is_correct else "WRONG"
        
        print(f"  {class_name}")
        print(f"    Predicted: {predicted_class} ({confidence:.1f}%)")
        print(f"    Disease: {disease_name}")
        print(f"    Status: {status}")

print("\n" + "="*80)
