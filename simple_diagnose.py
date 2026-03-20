import os
import pickle
import numpy as np
from PIL import Image

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
scaler = model_data['scaler']
class_names = model_data['class_names']

print("\n" + "="*80)
print("MODEL DIAGNOSTIC - SIMPLE VERSION")
print("="*80)

# Test with one image from each crop
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_cases = [
    ('Corn___healthy', 'Corn'),
    ('Grape___healthy', 'Grape'),
    ('Pepper___healthy', 'Pepper'),
    ('Potato___healthy', 'Potato'),
    ('Tomato___healthy', 'Tomato'),
]

print("\nTesting model predictions:\n")

for folder, crop_name in test_cases:
    folder_path = os.path.join(dataset_path, folder)
    
    # Get first original image
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"NO IMAGES in {folder}")
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    # Load and preprocess
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.flatten().reshape(1, -1)
    
    # Normalize
    img_scaled = scaler.transform(img_array)
    
    # Predict
    predictions = model.predict_proba(img_scaled)[0]
    predicted_idx = np.argmax(predictions)
    predicted_class = class_names[predicted_idx]
    confidence = predictions[predicted_idx] * 100
    
    # Check if correct
    is_correct = crop_name in predicted_class
    status = "CORRECT" if is_correct else "WRONG"
    
    print(f"{crop_name} Test:")
    print(f"  Expected: {folder}")
    print(f"  Got: {predicted_class}")
    print(f"  Confidence: {confidence:.2f}%")
    print(f"  Status: {status}")
    print()

print("="*80)
