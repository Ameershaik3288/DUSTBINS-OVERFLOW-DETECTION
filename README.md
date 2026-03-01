# 🗑️ Dustbin Overflow Detection using CNN

An AI-powered Smart City solution that detects dustbin overflow using
Convolutional Neural Networks (CNN).

## 🚀 Project Overview

This project classifies dustbin images into: - Overflow - Normal

It provides a web interface for real-time image upload and prediction.

------------------------------------------------------------------------

## 📁 Project Structure

dustbin_app/ 

├── app.py 

├── dustbin_overflow_cnn.h5

├── static/ 

  └── uploads/

├── templates/ 

  └──index.html
  
  └──result.html


└── README.md

------------------------------------------------------------------------

## ⚙️ How to Run

1.  Install dependencies: pip install flask tensorflow numpy pillow

2.  Run application: python app.py

3.  Open browser: http://127.0.0.1:5000/
   
4.  Download CNN Image Trained Model from Drive : https://drive.google.com/file/d/1zdG_ceI4xJj9O7P36pVB1a_jCIXmF5cO/view?usp=drive_link

------------------------------------------------------------------------

## 🧠 Model Details

-   Model Type: CNN
-   Framework: TensorFlow / Keras
-   Dataset: 50 Overflow + 50 Normal images
-   Output: Binary Classification

------------------------------------------------------------------------

## 🏆 Hackathon Ready

This system can be extended to send alerts to municipality and cleaning
workers for smart waste management.
