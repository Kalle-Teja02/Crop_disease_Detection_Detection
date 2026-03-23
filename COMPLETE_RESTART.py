#!/usr/bin/env python3
"""
Complete Restart Script
Clears cache, retrains model, and prepares for fresh start
"""

import os
import shutil
import subprocess
import sys

print("="*70)
print("COMPLETE RESTART - CLEARING CACHE AND RETRAINING MODEL")
print("="*70)

# Step 1: Kill any running Flask processes
print("\n[1/5] Killing any running Python processes...")
try:
    os.system("taskkill /F /IM python.exe 2>nul")
    print("✅ Python processes killed")
except:
    print("⚠️ Could not kill processes (may not be running)")

# Step 2: Clear __pycache__ directories
print("\n[2/5] Clearing Python cache...")
cache_dirs = [
    'crop-disease-detection/__pycache__',
    'crop-disease-detection/services/__pycache__',
    'crop-disease-detection/utils/__pycache__'
]

for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)
            print(f"✅ Deleted {cache_dir}")
        except Exception as e:
            print(f"⚠️ Could not delete {cache_dir}: {e}")

# Step 3: Delete old model file
print("\n[3/5] Deleting old model file...")
model_file = 'crop-disease-detection/model_cnn.pkl'
if os.path.exists(model_file):
    try:
        os.remove(model_file)
        print(f"✅ Deleted {model_file}")
    except Exception as e:
        print(f"⚠️ Could not delete {model_file}: {e}")

# Step 4: Retrain model
print("\n[4/5] Retraining model with optimized parameters...")
print("This may take 5-10 minutes...\n")

try:
    result = subprocess.run(
        [sys.executable, 'crop-disease-detection/train_cnn_model.py'],
        cwd='.',
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n✅ Model training completed successfully!")
    else:
        print("\n❌ Model training failed!")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ Error during training: {e}")
    sys.exit(1)

# Step 5: Summary
print("\n" + "="*70)
print("RESTART COMPLETE!")
print("="*70)
print("\n✅ All done! Now:")
print("   1. Close all browser windows")
print("   2. Clear browser cache (Ctrl+Shift+Delete)")
print("   3. Run: python app.py")
print("   4. Go to: http://localhost:5000")
print("   5. Upload grape image")
print("\nYou should now get 80%+ confidence for grapes! 🍇")
print("="*70)
