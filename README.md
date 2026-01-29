Product Damage Detection (Classical Image Processing)

This project implements a classical image processing–based system to detect and highlight surface anomalies (possible damage) on rigid products using a single input image.
The application is built using Python, OpenCV, and Flask as part of an Image Processing academic assignment and is intended for learning and demonstration purposes.


FEATURES
- Single image upload via Flask web interface
- Automatic product region isolation using contour detection
- Edge-based damage highlighting
- Morphological noise reduction
- Damage area estimation relative to product area
- ACCEPT / REJECT condition output


TECH STACK
- Python
- OpenCV
- NumPy
- Flask


PROJECT STRUCTURE
IP/
├── README.md
└── project/
    ├── app.py
    ├── main.py
    └── templates/
        └── index.html


SETUP & RUN
git clone https://github.com/karunrajkumar16/Product-Damage-Detection-using-Classical-Image-Processing.git
cd Product-Damage-Detection-using-Classical-Image-Processing
pip install -r requirements.txt
python project/app.py


Open your browser and visit:
http://127.0.0.1:5000/


HOW IT WORKS
- The input image is converted to grayscale and blurred
- Edges are detected using Canny edge detection
- Morphological operations are applied to reduce noise
- The largest contour is extracted as the product region
- Damage regions are highlighted and evaluated


LIMITATIONS
- Sensitive to lighting variations
- Edge-based detection may flag textures or logos as damage
- Uses fixed thresholding
- Not suitable for production use


DEPLOYMENT
This application is tested and deployed locally using Flask.


LICENSE
MIT License
