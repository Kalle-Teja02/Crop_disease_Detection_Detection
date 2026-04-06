from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from dotenv import load_dotenv
from disease_info import disease_data
from services.prediction_service import PredictionService
from services.storage_service import StorageService

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['HISTORY_FILE'] = os.path.join(os.path.dirname(__file__), 'detection_history.json')

# Initialize StorageService with MySQL
storage_service = StorageService(
    json_path=app.config['HISTORY_FILE'],
    db_path=os.path.join(os.path.dirname(__file__), 'predictions.db'),
    mysql_config={
        'host':     os.getenv('MYSQL_HOST', 'localhost'),
        'user':     os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DB', 'crop_disease_db'),
    }
)

# Load PyTorch CNN model via PredictionService
print("Starting Flask app...")
prediction_service = PredictionService()
_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_cnn.pth')
_result = prediction_service.load_model(_model_path)
if _result['success']:
    print(f"✅ {_result['message']}")
else:
    print(f"❌ {_result['message']}")

def load_history():
    return storage_service.load_history_json()

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

@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    try:
        from generate_report import generate_pdf_report

        # Read all fields from the POST form
        image_path_raw = request.form.get('image_path', '')
        disease_name   = request.form.get('disease_name', 'Unknown')
        confidence     = request.form.get('confidence', '0')
        symptoms       = request.form.get('symptoms', 'N/A')
        causes         = request.form.get('causes', 'N/A')
        treatment      = request.form.get('treatment', 'N/A')
        prevention     = request.form.get('prevention', 'N/A')
        pesticides     = request.form.get('pesticides', 'N/A')
        organic_solutions = request.form.get('organic_solutions', 'N/A')

        # Resolve image path
        filename = image_path_raw.replace('uploads/', '').replace('uploads\\', '')
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Create reports directory inside app folder
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        pdf_filename = filename.rsplit('.', 1)[0] + '_report.pdf'
        pdf_path = os.path.join(reports_dir, pdf_filename)

        generate_pdf_report(
            image_path=image_path if os.path.exists(image_path) else None,
            disease_name=disease_name,
            symptoms=symptoms,
            causes=causes,
            treatment=treatment,
            prevention=prevention,
            pesticides=pesticides,
            organic_solutions=organic_solutions,
            confidence=float(confidence),
            output_path=pdf_path
        )

        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating report: {str(e)}", 500

@app.route('/generate-report-history', methods=['POST'])
def generate_report_history():
    try:
        from generate_report import generate_pdf_report

        image_path_raw = request.form.get('image_path', '')
        disease_name   = request.form.get('disease_name', 'Unknown')
        confidence     = request.form.get('confidence', '0')

        # Look up disease details by display name
        disease_info = next(
            (v for v in disease_data.values() if v.get('name') == disease_name),
            {}
        )

        symptoms          = disease_info.get('symptoms', 'N/A')
        causes            = disease_info.get('causes', 'N/A')
        treatment         = disease_info.get('treatment', 'N/A')
        prevention        = disease_info.get('prevention', 'N/A')
        pesticides        = disease_info.get('pesticides', 'N/A')
        organic_solutions = disease_info.get('organic_solutions', 'N/A')

        filename   = image_path_raw.replace('uploads/', '').replace('uploads\\', '')
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        pdf_filename = filename.rsplit('.', 1)[0] + '_report.pdf'
        pdf_path     = os.path.join(reports_dir, pdf_filename)

        generate_pdf_report(
            image_path=image_path if os.path.exists(image_path) else None,
            disease_name=disease_name,
            symptoms=symptoms,
            causes=causes,
            treatment=treatment,
            prevention=prevention,
            pesticides=pesticides,
            organic_solutions=organic_solutions,
            confidence=float(confidence),
            output_path=pdf_path
        )

        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating report: {str(e)}", 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    storage_service.clear_history()
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return redirect(url_for('history'))

@app.route('/delete-result/<filename>', methods=['POST'])
def delete_result(filename):
    try:
        storage_service.delete_prediction(filename)

        # Delete the image file
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete associated PDF report if exists
        pdf_filename = filename.rsplit('.', 1)[0] + '_report.pdf'
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports', pdf_filename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        return redirect(url_for('history'))
    except Exception as e:
        return f"Error deleting result: {str(e)}", 500

@app.route('/predict', methods=['POST'])
def predict():
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

        # Run prediction via PredictionService
        result = prediction_service.predict(filepath)

        if result['success']:
            predicted_class = result['label']
            confidence = result['confidence']
        else:
            print(f"Prediction error: {result['error']}")
            return f"Prediction failed: {result['error']}", 500

        # Get disease information
        disease_info = disease_data.get(predicted_class, {
            'name': predicted_class.replace('___', ' - ').replace('_', ' '),
            'symptoms': 'Information not available',
            'treatment': 'Consult agricultural expert'
        })

        # Save to history (JSON + SQLite + MySQL)
        storage_service.save_prediction(filepath, disease_info['name'], round(confidence, 2))

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
                               demo_mode=False)

    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)
