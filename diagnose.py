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

print("=" * 80)
print("MODEL DIAGNOSTIC")
print("=" * 80)
print(f"\nModel type: {type(model)}")
print(f"Number of classes: {len(class_names)}")
print(f"Classes: {class_names}\n")

# Check feature importance
if hasattr(model, 'feature_importances_'):
    print(f"Feature importances shape: {model.feature_importances_.shape}")
    print(f"Top 10 important features: {np.argsort(model.feature_importances_)[-10:]}")

# Test with random images
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')

print("\n" + "=" * 80)
print("TESTING WITH RANDOM IMAGES FROM EACH CLASS")
print("=" * 80)

for class_idx, class_name in enumerate(class_names):
    folder_path = os.path.join(dataset_path, class_name)
    
    # Get first original image
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) 
                  and not any(x in f for x in ['_flip', '_rot', '_bright', '_dark', '_zoom', '_blur'])]
    
    if not image_files:
        print(f"\n❌ No images in {class_name}")
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
    
    # Get raw predictions
    predictions = model.predict_proba(img_scaled)[0]
    predicted_idx = np.argmax(predictions)
    
    print(f"\nClass {class_idx}: {class_name}")
    print(f"  Expected: {class_idx}, Got: {predicted_idx}")
    print(f"  Confidence: {predictions[predicted_idx]*100:.2f}%")
    
    if predicted_idx == class_idx:
        print(f"  ✅ CORRECT")
    else:
        print(f"  ❌ WRONG - Predicted {class_names[predicted_idx]}")
        print(f"  All predictions: {[(class_names[i], predictions[i]*100) for i in np.argsort(predictions)[-5:][::-1]]}")

print("\n" + "=" * 80)
