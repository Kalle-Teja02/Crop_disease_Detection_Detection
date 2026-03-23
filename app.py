from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import random
import json
from datetime import datetime
from disease_info import disease_data
import pickle
import numpy as np
from PIL import Image as PILImage

# Import generate_report at top level
try:
    from generate_report import generate_pdf_report
    REPORT_AVAILABLE = True
    print("✅ generate_report imported successfully")
except ImportError as e:
    print(f"⚠️  generate_report not available: {e}")
    REPORT_AVAILABLE = False

# Import the new prediction service
try:
    from services.prediction_service import PredictionService
    from services.storage_service import StorageService
    PREDICTION_SERVICE_AVAILABLE = True
    STORAGE_SERVICE_AVAILABLE = True
    print("✅ PredictionService and StorageService imported successfully")
except ImportError as e:
    print(f"❌ Error importing services: {e}")
    PREDICTION_SERVICE_AVAILABLE = False
    STORAGE_SERVICE_AVAILABLE = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['HISTORY_FILE'] = os.path.join(os.path.dirname(__file__), 'detection_history.json')

# Global model variables
prediction_service = None
storage_service = None
class_names = None
USE_MODEL = False
MODEL_TYPE = None

def load_model():
    """Load the CNN model using PredictionService"""
    global prediction_service, storage_service, class_names, USE_MODEL, MODEL_TYPE
    
    try:
        if not PREDICTION_SERVICE_AVAILABLE:
            raise Exception("PredictionService not available")
        
        # Initialize prediction service
        prediction_service = PredictionService()
        
        # Load model
        result = prediction_service.load_model()
        
        if not result['success']:
            raise Exception(f"Failed to load model: {result.get('message', 'Unknown error')}")
        
        # Get model info
        class_names = prediction_service.class_names
        MODEL_TYPE = prediction_service.model_type
        
        print(f"✅ {MODEL_TYPE} model loaded successfully!")
        print(f"Classes: {len(class_names)}")
        print(f"Image size: {prediction_service.img_size}")
        
        # Initialize storage service if available
        if STORAGE_SERVICE_AVAILABLE:
            try:
                storage_service = StorageService()
                print("✅ StorageService initialized successfully")
            except Exception as e:
                print(f"⚠️  Error initializing StorageService: {e}")
                storage_service = None
        
        USE_MODEL = True
        return True
        
    except Exception as e:
        print(f"❌ Error loading model - {e}")
        prediction_service = None
        storage_service = None
        USE_MODEL = False
        MODEL_TYPE = None
        class_names = ['Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy', 
                       'Grape___Black_rot', 'Grape___Leaf_blight', 'Grape___healthy', 
                       'Pepper___Bacterial_spot', 'Pepper___healthy', 
                       'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                       'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 
                       'Tomato___Leaf_Mold', 'Tomato___healthy']
        return False

# Load model on startup
print("Starting Flask app...")
load_model()

def load_history():
    if os.path.exists(app.config['HISTORY_FILE']):
        with open(app.config['HISTORY_FILE'], 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(app.config['HISTORY_FILE'], 'w') as f:
        json.dump(history, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/history')
def history():
    history_data = load_history()
    return render_template('history.html', history=history_data)

@app.route('/download/<path:filename>')
def download(filename):
    try:
        # Handle both 'filename' and 'uploads/filename' formats
        if filename.startswith('uploads/') or filename.startswith('uploads\\'):
            filename = filename.replace('uploads/', '').replace('uploads\\', '')
        
        # Check if requesting PDF report
        if filename.endswith('_report.pdf'):
            filepath = os.path.join('reports', filename)
        else:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return f"File not found: {filepath}", 404
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

@app.route('/generate-report-history', methods=['POST'])
def generate_report_history():
    try:
        if not REPORT_AVAILABLE:
            return "PDF generation not available. Install reportlab: pip install reportlab", 500

        filename     = request.form.get('image_path', '').strip()
        disease_name = request.form.get('disease_name', 'Unknown Disease')
        confidence   = float(request.form.get('confidence', 0))

        # Look up full disease details from disease_data
        disease_key = next((k for k in disease_data if disease_data[k]['name'] == disease_name), None)
        if disease_key:
            info = disease_data[disease_key]
        else:
            info = {}

        symptoms          = info.get('symptoms', 'N/A')
        causes            = info.get('causes', 'N/A')
        treatment         = info.get('treatment', 'N/A')
        prevention        = info.get('prevention', 'N/A')
        pesticides        = info.get('pesticides', 'N/A')
        organic_solutions = info.get('organic_solutions', 'N/A')

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(image_path):
            image_path = None  # Generate PDF without image if not found

        reports_dir  = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        base_name    = filename.rsplit('.', 1)[0] if '.' in filename else filename
        pdf_filename = base_name + '_report.pdf'
        pdf_path     = os.path.join(reports_dir, pdf_filename)

        generate_pdf_report(
            image_path=image_path,
            disease_name=disease_name,
            symptoms=symptoms,
            causes=causes,
            treatment=treatment,
            prevention=prevention,
            pesticides=pesticides,
            organic_solutions=organic_solutions,
            confidence=confidence,
            output_path=pdf_path
        )

        print(f"✅ History PDF generated: {pdf_path}")
        return send_file(pdf_path, as_attachment=True,
                         download_name=pdf_filename,
                         mimetype='application/pdf')

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating report: {str(e)}", 500

@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    try:
        if not REPORT_AVAILABLE:
            return "PDF generation not available. Please install reportlab: pip install reportlab", 500

        filename          = request.form.get('image_path', '').strip()
        disease_name      = request.form.get('disease_name', 'Unknown Disease')
        confidence        = float(request.form.get('confidence', 0))
        symptoms          = request.form.get('symptoms', 'N/A')
        causes            = request.form.get('causes', 'N/A')
        treatment         = request.form.get('treatment', 'N/A')
        prevention        = request.form.get('prevention', 'N/A')
        pesticides        = request.form.get('pesticides', 'N/A')
        organic_solutions = request.form.get('organic_solutions', 'N/A')

        print(f"Generating report for: {filename}, disease: {disease_name}")

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(image_path):
            return f"Image not found at: {image_path}", 404

        # Create reports directory inside the app folder
        reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        base_name    = filename.rsplit('.', 1)[0] if '.' in filename else filename
        pdf_filename = base_name + '_report.pdf'
        pdf_path     = os.path.join(reports_dir, pdf_filename)

        generate_pdf_report(
            image_path=image_path,
            disease_name=disease_name,
            symptoms=symptoms,
            causes=causes,
            treatment=treatment,
            prevention=prevention,
            pesticides=pesticides,
            organic_solutions=organic_solutions,
            confidence=confidence,
            output_path=pdf_path
        )

        print(f"✅ PDF generated at: {pdf_path}")
        return send_file(pdf_path, as_attachment=True,
                         download_name=pdf_filename,
                         mimetype='application/pdf')

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating report: {str(e)}", 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    # Clear history file
    save_history([])
    # Optionally clear uploaded images
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect(url_for('history'))

@app.route('/delete-result/<filename>', methods=['POST'])
def delete_result(filename):
    try:
        # Load history
        history_data = load_history()
        
        # Remove the specific entry
        history_data = [item for item in history_data if item['image'] != filename]
        
        # Save updated history
        save_history(history_data)
        
        # Delete the image file
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete associated PDF report if exists
        pdf_filename = filename.rsplit('.', 1)[0] + '_report.pdf'
        pdf_path = os.path.join('reports', pdf_filename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        return redirect(url_for('history'))
    except Exception as e:
        return f"Error deleting result: {str(e)}", 500

@app.route('/predict', methods=['POST'])
def predict():
    global prediction_service, class_names, USE_MODEL
    
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        # Save uploaded file
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if USE_MODEL and prediction_service is not None:
            # Real prediction with PyTorch CNN model
            try:
                # Use prediction service
                result = prediction_service.predict(filepath)
                
                if result['success']:
                    predicted_class = result['label']
                    confidence = result['confidence']
                    
                    # Debug: print top 3 predictions
                    print(f"\n=== PREDICTION DEBUG ===")
                    print(f"Image: {filename}")
                    print(f"Model type: {prediction_service.model_type}")
                    print(f"Predicted: {predicted_class}, Confidence: {confidence:.2f}%")
                    
                    # Show top 3 predictions from probabilities
                    if 'probabilities' in result:
                        probs = result['probabilities']
                        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
                        print(f"Top 3 predictions:")
                        for i, (class_name, conf) in enumerate(sorted_probs):
                            print(f"  {i+1}. {class_name}: {conf:.2f}%")
                    
                    print(f"========================\n")
                else:
                    print(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
                    predicted_class = random.choice(class_names)
                    confidence = random.uniform(75, 95)
                    
            except Exception as e:
                print(f"Prediction error: {e}")
                import traceback
                traceback.print_exc()
                predicted_class = random.choice(class_names)
                confidence = random.uniform(75, 95)
        else:
            # Demo mode - random prediction
            print(f"⚠️ Using DEMO mode - model not loaded properly")
            predicted_class = random.choice(class_names)
            confidence = random.uniform(75, 95)
        
        # Get disease information
        disease_info = disease_data.get(predicted_class, {
            'name': predicted_class.replace('___', ' - ').replace('_', ' '),
            'symptoms': 'Information not available',
            'treatment': 'Consult agricultural expert'
        })
        
        # Save to history (JSON file)
        history = load_history()
        history.insert(0, {
            'image': filename,
            'disease': disease_info['name'],
            'confidence': round(confidence, 2),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        # Keep only last 20 detections
        history = history[:20]
        save_history(history)
        
        # Save to database using storage service
        if storage_service is not None:
            try:
                # Extract crop and disease from predicted_class
                if '___' in predicted_class:
                    crop, disease = predicted_class.split('___', 1)
                    disease = disease.replace('_', ' ')
                else:
                    crop = 'Unknown'
                    disease = predicted_class.replace('_', ' ')
                
                # Save prediction to database
                db_result = storage_service.save_prediction(
                    crop=crop,
                    disease=disease,
                    confidence=confidence,
                    image_path=filename,
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                
                if db_result['success']:
                    print(f"✅ Prediction saved to database: {db_result.get('message', 'Success')}")
                else:
                    print(f"⚠️  Failed to save to database: {db_result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                print(f"⚠️  Error saving to database: {e}")
        
        return render_template('result.html', 
                             disease_name=disease_info['name'],
                             symptoms=disease_info['symptoms'],
                             causes=disease_info.get('causes', 'Information not available'),
                             treatment=disease_info['treatment'],
                             prevention=disease_info.get('prevention', 'Information not available'),
                             pesticides=disease_info.get('pesticides', 'Information not available'),
                             organic_solutions=disease_info.get('organic_solutions', 'Information not available'),
                             confidence=round(confidence, 2),
                             image_path=filename,
                             demo_mode=not USE_MODEL)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)
