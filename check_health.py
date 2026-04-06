"""Health check - run this anytime to verify everything is working"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== Crop Disease Detection - Health Check ===\n")

# 1. Check critical files
critical_files = [
    'model_cnn.pth',
    'model_metadata.pkl',
    'app.py',
    'disease_info.py',
    'generate_report.py',
    'services/prediction_service.py',
    'services/recommendation_service.py',
    'services/storage_service.py',
    'utils/preprocessing.py',
    'templates/index.html',
    'templates/detect.html',
    'templates/result.html',
    'templates/history.html',
    'static/style.css',
]
all_ok = True
for f in critical_files:
    exists = os.path.exists(f)
    status = 'OK' if exists else 'MISSING'
    if not exists:
        all_ok = False
    print(f'  [{status}] {f}')

# 2. Check model loads
print("\n--- Model Load ---")
try:
    from services.prediction_service import PredictionService
    svc = PredictionService()
    result = svc.load_model('model_cnn.pth')
    if result['success']:
        print(f"  [OK] Model loaded: {svc.model_type}, img_size={svc.img_size}, classes={len(svc.class_names)}")
    else:
        print(f"  [FAIL] {result['message']}")
        all_ok = False
except Exception as e:
    print(f"  [FAIL] {e}")
    all_ok = False

# 3. Quick prediction test
print("\n--- Prediction Test ---")
try:
    test_img = os.path.join('..', 'dataset', 'Corn___Common_rust', 'img_1.jpg')
    if os.path.exists(test_img):
        r = svc.predict(test_img)
        if r['success']:
            print(f"  [OK] Corn rust -> {r['label']} ({round(r['confidence'],1)}%)")
        else:
            print(f"  [FAIL] {r['error']}")
            all_ok = False
    else:
        print("  [SKIP] Dataset not found (OK for production)")
except Exception as e:
    print(f"  [FAIL] {e}")
    all_ok = False

# 4. Check imports
print("\n--- Imports ---")
for module in ['flask', 'torch', 'PIL', 'reportlab', 'numpy']:
    try:
        __import__(module)
        print(f"  [OK] {module}")
    except ImportError:
        print(f"  [MISSING] {module} - run: pip install {module}")
        all_ok = False

print("\n" + ("=== ALL GOOD - Ready to run ===" if all_ok else "=== ISSUES FOUND - Fix above errors ==="))
print("\nTo start: python app.py")
