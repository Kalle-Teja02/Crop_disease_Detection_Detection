#!/usr/bin/env python
"""
Force restart Flask app with new model
"""

import os
import sys
import subprocess
import time

print("\n" + "="*80)
print("RESTARTING FLASK APP WITH NEW MODEL")
print("="*80)

# Step 1: Kill all Python processes
print("\n[1/4] Killing all Python processes...")
os.system("taskkill /F /IM python.exe 2>nul")
time.sleep(3)
print("  Done")

# Step 2: Verify new model
print("\n[2/4] Verifying new model...")
model_path = os.path.join(os.path.dirname(__file__), 'model_cnn.pkl')
size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"  Model size: {size_mb:.1f} MB")
if size_mb > 50:
    print("  OK - This is the new trained model (was 1.77 MB before)")
else:
    print("  ERROR - Model size is too small!")
    sys.exit(1)

# Step 3: Test model
print("\n[3/4] Testing model predictions...")
result = subprocess.run([sys.executable, "crop-disease-detection/simulate_app.py"], 
                       capture_output=True, text=True, timeout=60)
if "Correct: YES" in result.stdout:
    print("  Model working correctly")
else:
    print("  ERROR - Model not working")
    sys.exit(1)

# Step 4: Start Flask
print("\n[4/4] Starting Flask app...")
print("\n" + "="*80)
print("Flask is starting. Wait for: 'Running on http://localhost:5000'")
print("="*80 + "\n")

os.system("python crop-disease-detection/app.py")
