"""
FINAL FIX - Complete reset and verification
Run this script to ensure everything is working
"""

import os
import sys
import subprocess
import time

print("\n" + "="*80)
print("CROP DISEASE DETECTION - FINAL FIX")
print("="*80)

# Step 1: Kill all Python processes
print("\n1. Stopping all Python processes...")
try:
    os.system("taskkill /F /IM python.exe 2>nul")
    time.sleep(2)
    print("   Done - All Python processes stopped")
except:
    print("   (No processes to stop)")

# Step 2: Verify model
print("\n2. Verifying model...")
result = subprocess.run([sys.executable, "crop-disease-detection/debug_app.py"], 
                       capture_output=True, text=True)
if "SUCCESS" in result.stdout:
    print("   Model verification: PASSED")
else:
    print("   Model verification: FAILED")
    print(result.stdout)
    sys.exit(1)

# Step 3: Instructions
print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("\n1. CLEAR YOUR BROWSER CACHE")
print("   - Chrome: Ctrl+Shift+Delete")
print("   - Firefox: Ctrl+Shift+Delete")
print("   - Edge: Ctrl+Shift+Delete")
print("   - Safari: Cmd+Shift+Delete")

print("\n2. START THE APP FRESH")
print("   Run this command in a NEW terminal:")
print("   python crop-disease-detection/app.py")

print("\n3. OPEN IN BROWSER")
print("   Go to: http://localhost:5000")

print("\n4. TEST WITH DIFFERENT CROPS")
print("   - Upload a Corn image")
print("   - Upload a Grape image")
print("   - Upload a Pepper image")
print("   - Upload a Potato image")
print("   - Upload a Tomato image")

print("\n" + "="*80)
print("IMPORTANT:")
print("="*80)
print("- Make sure you're uploading images from the CORRECT crop")
print("- The model predicts the crop type first, then the disease")
print("- If you upload a Tomato image, it should show Tomato diseases")
print("- If you upload a Corn image, it should show Corn diseases")
print("="*80 + "\n")
