#!/usr/bin/env python
"""
Quick status check - shows if everything is ready
"""

import os
import pickle

print("\n" + "="*60)
print("CROP DISEASE DETECTION - STATUS CHECK")
print("="*60)

# Check model
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"\nModel file: OK ({size_mb:.2f} MB)")
    
    try:
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
        print(f"Model classes: {len(data['class_names'])}")
        print(f"Model type: {type(data['model']).__name__}")
    except:
        print("Model file: CORRUPTED")
else:
    print("\nModel file: NOT FOUND")

# Check app
app_path = os.path.join(os.path.dirname(__file__), 'app.py')
if os.path.exists(app_path):
    print(f"App file: OK")
else:
    print(f"App file: NOT FOUND")

# Check disease data
try:
    from disease_info import disease_data
    print(f"Disease data: OK ({len(disease_data)} diseases)")
except:
    print(f"Disease data: ERROR")

print("\n" + "="*60)
print("Ready to start? Run:")
print("  python crop-disease-detection/app.py")
print("="*60 + "\n")
