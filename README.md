# Crop Disease Detection System

Detects diseases in corn, grape, pepper, potato, and tomato leaves using a PyTorch CNN model.

## How to Start

```bash
cd crop-disease-detection
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Health Check

Run this anytime to verify everything is working before starting:

```bash
python check_health.py
```

## Install Dependencies (first time only)

```bash
pip install -r requirements.txt
```

## Supported Crops & Diseases

| Crop    | Diseases                                      |
|---------|-----------------------------------------------|
| Corn    | Common Rust, Northern Leaf Blight, Healthy    |
| Grape   | Black Rot, Leaf Blight, Healthy               |
| Pepper  | Bacterial Spot, Healthy                       |
| Potato  | Early Blight, Late Blight, Healthy            |
| Tomato  | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Healthy |

## Features

- Upload a leaf image → get disease prediction with confidence score
- Full disease details: symptoms, causes, treatment, prevention, pesticides, organic solutions
- Download PDF report with all details
- Detection history with per-entry PDF download
