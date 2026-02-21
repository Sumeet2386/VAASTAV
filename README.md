VAASTAV – Media & Certificate Verification System
VAASTAV is a full-stack AI-based verification platform designed to detect manipulated or AI-generated media content. The system supports verification of images, videos, audio files, and digital certificates through a unified interface.

The project combines machine learning models, signal processing techniques, and rule-based validation to provide authenticity analysis with confidence scores.

Features :-
Image Verification
Detects AI-generated or manipulated images
Uses pretrained CNN-based models
Returns confidence score and reasoning
Video Verification
Extracts frames from video
Performs frame-level deepfake analysis
Aggregates results for final verdict
Audio Verification
Detects AI-generated or synthetic voices
Uses pitch analysis, MFCC, spectral features, and silence detection
Classifies audio as likely human or AI-generated
Certificate Verification
OCR-based text extraction
QR code detection and validation
Roll number and name integrity checks
Confidence-based authenticity scoring
Tech Stack
Frontend
React (Vite)
JavaScript
Backend
FastAPI
Python
Machine Learning & Processing
Scikit-learn
OpenCV
Librosa
NumPy / SciPy
Tesseract OCR
Project Structure

How to Run 
Backend :-

cd backend,
pip install -r requirements.txt,
uvicorn app.main:app --reload


Backend runs on:

http://127.0.0.1:8000

Frontend :-

cd frontend,
npm install,
npm run dev


Frontend runs on:

http://localhost:5173

Use Cases:-
Deepfake detection,

AI voice scam detection,

Certificate authenticity validation,

Media integrity verification
