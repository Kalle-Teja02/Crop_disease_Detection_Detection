import os
import pickle
import numpy as np
from PIL import Image
from disease_info import disease_data

# Load model exactly like app.py does
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
scaler = model_data['scaler']
class_names = model_data['class_names']

print("\n" + "="*80)
print("FULL APP FLOW TEST - SIMULATING EXACT APP BEHAVIOR")
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

print("\nSimulating app.py predict() function:\n")

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
    
    # EXACT app.py logic
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.flatten().reshape(1, -1)
    
    img_scaled = scaler.transform(img_array)
    
    predictions = model.predict_proba(img_scaled)[0]
    prediction_idx = np.argmax(predictions)
    confidence = predictions[prediction_idx] * 100
    
    predicted_class = class_names[int(prediction_idx)]
    
    # EXACT app.py disease lookup
    disease_info = disease_data.get(predicted_class, {
        'name': predicted_class.replace('___', ' - ').replace('_', ' '),
        'symptoms': 'Information not available',
        'treatment': 'Consult agricultural expert'
    })
    
    disease_name = disease_info['name']
    
    # Check if correct
    is_correct = crop_name in predicted_class
    
    print(f"{crop_name} Test:")
    print(f"  Image: {img_file}")
    print(f"  Predicted class: {predicted_class}")
    print(f"  Disease name shown: {disease_name}")
    print(f"  Confidence: {confidence:.2f}%")
    print(f"  Correct: {'YES' if is_correct else 'NO'}")
    print()

print("="*80)
