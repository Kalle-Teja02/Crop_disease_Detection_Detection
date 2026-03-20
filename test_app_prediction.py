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

print("=" * 80)
print("SIMULATING APP PREDICTION")
print("=" * 80)

# Test with one image from each crop
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
    
    # Get first original image
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"\n❌ No images in {folder}")
        continue
    
    img_file = image_files[0]
    img_path = os.path.join(folder_path, img_file)
    
    # Load and preprocess (EXACTLY like app.py does)
    img = Image.open(img_path).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.flatten().reshape(1, -1)
    
    # Normalize (EXACTLY like app.py does)
    img_scaled = scaler.transform(img_array)
    
    # Get prediction (EXACTLY like app.py does)
    predictions = model.predict_proba(img_scaled)[0]
    prediction_idx = np.argmax(predictions)
    confidence = predictions[prediction_idx] * 100
    
    predicted_class = class_names[int(prediction_idx)]
    
    print(f"\n{crop_name} Test:")
    print(f"  Predicted class: {predicted_class}")
    print(f"  Confidence: {confidence:.2f}%")
    
    # Check disease_data lookup
    disease_info = disease_data.get(predicted_class, None)
    
    if disease_info:
        print(f"  ✅ Found in disease_data: {disease_info['name']}")
    else:
        print(f"  ❌ NOT found in disease_data!")
        print(f"  Available keys in disease_data:")
        for key in disease_data.keys():
            if crop_name in key:
                print(f"    - {key}")

print("\n" + "=" * 80)
print("CHECKING ALL CLASS NAMES IN DISEASE_DATA")
print("=" * 80)

missing = []
for class_name in class_names:
    if class_name not in disease_data:
        missing.append(class_name)
        print(f"❌ {class_name} - NOT in disease_data")
    else:
        print(f"✅ {class_name} - Found")

if missing:
    print(f"\n⚠️ MISSING {len(missing)} classes in disease_data!")
else:
    print(f"\n✅ All {len(class_names)} classes found in disease_data")
