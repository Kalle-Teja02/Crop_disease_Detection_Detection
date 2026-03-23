# Crop Disease Detection System

A web application for detecting crop diseases from images. Upload a photo of your crop and get instant disease identification with treatment recommendations.

## Features

- Detect diseases in Corn, Tomato, Grape, Pepper, and Potato
- Upload images and get instant predictions
- View prediction history
- Generate disease reports with treatment information
- Automatic data storage

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the application:
```bash
python app.py
```

3. Open http://localhost:5000 in your browser

4. Upload a crop image to detect diseases

## Supported Crops

- Corn (Healthy, Common Rust, Northern Leaf Blight)
- Tomato (Healthy, Early Blight, Late Blight, Bacterial Spot, Leaf Mold)
- Grape (Healthy, Black Rot, Leaf Blight)
- Pepper (Healthy, Bacterial Spot)
- Potato (Healthy, Early Blight, Late Blight)

## Project Structure

```
crop-disease-detection/
├── app.py                    # Main application
├── train_cnn_model.py        # Model training
├── disease_info.py           # Disease information
├── generate_report.py        # Report generation
├── requirements.txt          # Dependencies
├── model_cnn.pkl            # Trained model
├── services/                # Service modules
├── utils/                   # Utility functions
├── templates/               # HTML pages
└── static/                  # CSS and uploads
```

## Database

The application stores predictions in:
- MySQL (primary database)
- SQLite (backup)
- JSON (history file)

To set up MySQL, run:
```bash
mysql -u root -p crop_disease_db < MYSQL_SETUP.sql
```

## Configuration

Create a `.env` file with your database settings:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=crop_disease_db
```

## Technologies

- Python with Flask
- MySQL and SQLite databases
- Machine learning model for disease detection
- HTML/CSS for web interface

## Usage

1. Upload a crop image
2. Get instant disease prediction
3. View treatment recommendations
4. Check prediction history

That's it! The application handles everything automatically.
