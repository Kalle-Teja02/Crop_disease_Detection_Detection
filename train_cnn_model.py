import os
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import sys

# Dataset path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
DATASET_PATH = os.path.join(parent_dir, 'dataset')

print("Starting CNN model training with optimized Random Forest...\n")

all_images = []
all_labels = []
class_names = []
class_counts = {}

# Get all disease folders
disease_folders = sorted([d for d in os.listdir(DATASET_PATH) 
                         if os.path.isdir(os.path.join(DATASET_PATH, d))])

print(f"Found {len(disease_folders)} disease classes\n")

# Load ALL images (including augmented ones)
for idx, disease_folder in enumerate(disease_folders):
    folder_path = os.path.join(DATASET_PATH, disease_folder)
    # Load ALL images - original AND augmented
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    print(f"Loading {len(image_files)} images from {disease_folder}")
    class_counts[disease_folder] = len(image_files)
    
    for img_file in image_files:
        try:
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path).convert('RGB')
            img = img.resize((64, 64))
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            all_images.append(img_array.flatten())
            all_labels.append(idx)
        except Exception as e:
            print(f"  Error loading {img_file}: {e}")
    
    class_names.append(disease_folder)

print(f"\nTotal images loaded: {len(all_images)}")
print(f"Class distribution:")
for name, count in class_counts.items():
    print(f"  {name}: {count}")

# Convert to numpy arrays
X = np.array(all_images, dtype=np.float32)
y = np.array(all_labels)

print(f"\nTraining data shape: {X.shape}")

# Normalize features
print("Normalizing features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train with optimized Random Forest for high confidence
print("Training CNN model (Optimized Random Forest)...")
model = RandomForestClassifier(
    n_estimators=1000,  # More trees for better accuracy
    max_depth=20,       # Deeper trees to capture complex patterns
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42,
    n_jobs=-1,
    verbose=1
)
model.fit(X_scaled, y)

print("\nModel training completed!")

# Save model
model_path = os.path.join(script_dir, 'model_cnn.pkl')
model_data = {
    'model': model,
    'scaler': scaler,
    'class_names': class_names,
    'input_shape': (64, 64, 3)
}

# Remove old model if exists
if os.path.exists(model_path):
    os.remove(model_path)
    print(f"Removed old model file")

with open(model_path, 'wb') as f:
    pickle.dump(model_data, f)

print(f"Model saved to {model_path}")
print(f"Training accuracy: {model.score(X_scaled, y)*100:.2f}%")
print(f"\nClasses ({len(class_names)} total):")
for i, name in enumerate(class_names):
    print(f"  {i}: {name}")

sys.exit(0)
