# Product Damage Detection (Classical Image Processing)

## Overview
This project implements a **classical image processing–based system** to detect and highlight **surface anomalies (possible damage)** on rigid products using a **single input image**.

The application is built using **Python, OpenCV, and Flask** as part of an **Image Processing academic assignment**. It is intended for **learning and demonstration purposes**.

---

## Features
- Single image upload via Flask web interface  
- Automatic product region isolation using contour detection  
- Edge-based damage highlighting  
- Morphological noise reduction  
- Damage area estimation relative to product area  
- **ACCEPT / REJECT** condition output  

---

## Tech Stack
- Python  
- OpenCV  
- NumPy  
- Flask  

---

## Project Structure
```text
IP/
├── README.md
└── project/
    ├── app.py
    ├── main.py
    └── templates/
        └── index.html
