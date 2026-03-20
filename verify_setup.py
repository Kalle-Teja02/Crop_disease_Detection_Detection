#!/usr/bin/env python
"""
Verification script to ensure everything is set up correctly
Run this before starting the Flask app
"""

import os
import pickle
import sys

print("\n" + "=" * 80)
print("CROP DISEASE DETECTION - SETUP VERIFICATION")
print("=" * 80)

# Check model file
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
print(f"\n1. Checking model file...")
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   ✅ Model file exists: {model_path}")
    print(f"   Size: {size_mb:.2f} MB")
    
    # Load and verify
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        model = model_data['model']
        scaler = model_data['scaler']
        class_names = model_data['class_names']
        
        print(f"   ✅ Model loaded successfully")
        print(f"   Classes: {len(class_names)}")
        print(f"   Model type: {type(model).__name__}")
        
        if len(class_names) == 16:
            print(f"   ✅ All 16 classes present")
        else:
            print(f"   ❌ ERROR: Expected 16 classes, got {len(class_names)}")
            sys.exit(1)
            
    except Exception as e:
        print(f"   ❌ ERROR loading model: {e}")
        sys.exit(1)
else:
    print(f"   ❌ Model file NOT found: {model_path}")
    sys.exit(1)

# Check disease_info
print(f"\n2. Checking disease_info.py...")
try:
    from disease_info import disease_data
    print(f"   ✅ disease_info.py loaded")
    print(f"   Diseases in database: {len(disease_data)}")
    
    # Check if all classes are in disease_data
    missing = [c for c in class_names if c not in disease_data]
    if missing:
        print(f"   ❌ ERROR: Missing {len(missing)} classes in disease_data:")
        for m in missing:
            print(f"      - {m}")
        sys.exit(1)
    else:
        print(f"   ✅ All {len(class_names)} classes found in disease_data")
        
except Exception as e:
    print(f"   ❌ ERROR loading disease_info: {e}")
    sys.exit(1)

# Check dataset
print(f"\n3. Checking dataset...")
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset')
if os.path.exists(dataset_path):
    folders = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    print(f"   ✅ Dataset folder exists")
    print(f"   Disease folders: {len(folders)}")
    
    if len(folders) == 16:
        print(f"   ✅ All 16 disease folders present")
    else:
        print(f"   ⚠️ WARNING: Expected 16 folders, got {len(folders)}")
else:
    print(f"   ⚠️ WARNING: Dataset folder not found (not critical for app)")

# Check Flask app
print(f"\n4. Checking Flask app...")
app_path = os.path.join(os.path.dirname(__file__), 'app.py')
if os.path.exists(app_path):
    print(f"   ✅ app.py exists")
else:
    print(f"   ❌ ERROR: app.py not found")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ ALL CHECKS PASSED - READY TO START FLASK APP")
print("=" * 80)
print("\nTo start the app, run:")
print("  python crop-disease-detection/app.py")
print("\nThen open: http://localhost:5000")
print("=" * 80 + "\n")
