#!/usr/bin/env python
"""
Check if the new high-confidence model is loaded
"""

import os
import pickle

print("\n" + "="*60)
print("MODEL CHECK")
print("="*60)

model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')

# Check file size
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"\nModel file: {model_path}")
    print(f"Size: {size_mb:.1f} MB")
    
    if size_mb > 50:
        print("Status: NEW MODEL (trained with 2,250 images)")
        print("Expected confidence: 83-100%")
    elif size_mb < 5:
        print("Status: OLD MODEL (trained with 250 images)")
        print("Expected confidence: 30-90%")
        print("\nYou need to retrain!")
        print("Run: python crop-disease-detection/train_cnn_model.py")
    else:
        print("Status: UNKNOWN")
    
    # Try to load
    try:
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
        print(f"Classes: {len(data['class_names'])}")
        print(f"Model type: {type(data['model']).__name__}")
    except Exception as e:
        print(f"Error loading: {e}")
else:
    print("Model file NOT FOUND!")

print("\n" + "="*60)
