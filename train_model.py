import os
import pickle
import numpy as np
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import glob

# Dataset path - check multiple locations
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

if os.path.exists(os.path.join(parent_dir, 'dataset')):
    DATASET_PATH = os.path.join(parent_dir, 'dataset')
elif os.path.exists('dataset'):
    DATASET_PATH = 'dataset'
elif os.path.exists('crop-disease-detection/dataset'):
    DATASET_PATH = 'crop-disease-detection/dataset'
else:
    DATASET_PATH = os.path.join(parent_dir, 'dataset')
    print(f"Warning: Dataset path not found. Using: {DATASET_PATH}")

def load_images_from_folder(folder_path, label):
    """Load all images from a folder and return as flattened arrays with labels"""
    images = []
    labels = []
    
    # Get all image files
    image_files = glob.glob(os.path.join(folder_path, '*.jpg')) + \
                  glob.glob(os.path.join(folder_path, '*.jpeg')) + \
                  glob.glob(os.path.join(folder_path, '*.png')) + \
                  glob.glob(os.path.join(folder_path, '*.webp'))
    
    print(f"Loading {len(image_files)} images from {folder_path}")
    
    for img_path in image_files:
        try:
            # Load and preprocess image
            img = Image.open(img_path).convert('RGB')
            img = img.resize((64, 64))
            img_array = np.array(img).flatten()
            
            # Normalize to 0-1
            img_array = img_array.astype(np.float32) / 255.0
            
            images.append(img_array)
            labels.append(label)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
    
    return images, labels

def train_model():
    """Train the model on all disease classes"""
    print("Starting model training...")
    print(f"Dataset path: {DATASET_PATH}")
    print(f"Dataset exists: {os.path.exists(DATASET_PATH)}")
    
    all_images = []
    all_labels = []
    class_names = []
    label_encoder = {}
    
    # Get all disease folders
    disease_folders = sorted([d for d in os.listdir(DATASET_PATH) 
                             if os.path.isdir(os.path.join(DATASET_PATH, d))])
    
    print(f"Found {len(disease_folders)} disease classes: {disease_folders}")
    
    # Create label mapping: disease_name -> numeric_label
    for idx, disease_folder in enumerate(disease_folders):
        label_encoder[disease_folder] = idx
        class_names.append(disease_folder)
    
    # Load images from each disease folder
    for disease_folder in disease_folders:
        folder_path = os.path.join(DATASET_PATH, disease_folder)
        numeric_label = label_encoder[disease_folder]
        images, labels = load_images_from_folder(folder_path, numeric_label)
        
        all_images.extend(images)
        all_labels.extend(labels)
        
        print(f"  {disease_folder}: {len(images)} images")
    
    print(f"\nTotal images loaded: {len(all_images)}")
    
    # Convert to numpy arrays
    X = np.array(all_images)
    y = np.array(all_labels)
    
    print(f"Training data shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    # Train Random Forest model with optimized parameters for small dataset
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,      # Reduced from 200
        max_depth=10,          # Reduced from 20
        min_samples_split=5,   # Added: minimum samples to split
        min_samples_leaf=2,    # Added: minimum samples in leaf
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    model.fit(X, y)
    
    print("Model training completed!")
    
    # Save model with label encoder for consistent predictions
    model_data = {
        'model': model,
        'class_names': class_names,
        'label_encoder': label_encoder,
        'input_shape': (64, 64, 3)
    }
    
    with open('model_sklearn.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved to model_sklearn.pkl")
    print(f"Classes: {class_names}")
    print(f"Label Encoder: {label_encoder}")
    
    # Print model accuracy on training data
    train_accuracy = model.score(X, y)
    print(f"Training accuracy: {train_accuracy:.2%}")

if __name__ == '__main__':
    train_model()
