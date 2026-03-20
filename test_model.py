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

print(f"Model loaded with {len(class_names)} classes")
print(f"Classes: {class_names}\n")

# Test with one image from each crop type
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

test_cases = [
    ('Corn___healthy', 'Corn'),
    ('Grape___healthy', 'Grape'),
    ('Pepper___healthy', 'Pepper'),
    ('Potato___healthy', 'Potato'),
    ('Tomato___healthy', 'Tomato'),
]

print("=" * 70)
print("TESTING MODEL WITH SAMPLE IMAGES")
print("=" * 70)

for folder, crop_name in test_cases:
    folder_path = os.path.join(dataset_path, folder)
    
    # Get first original image (not augmented)
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"\n❌ No images found in {folder}")
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
    top_3_indices = np.argsort(predictions)[-3:][::-1]
    
    print(f"\n{crop_name} Test ({img_file}):")
    print(f"  Top 3 predictions:")
    for i, idx in enumerate(top_3_indices):
        confidence = predictions[idx] * 100
        class_name = class_names[idx]
        is_correct = "✅" if crop_name in class_name else "❌"
        print(f"    {i+1}. {is_correct} {class_name}: {confidence:.2f}%")

print("\n" + "=" * 70)
