<div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: auto;">

<h1 style="text-align:center;">Product Damage Detection <br/><span style="font-size:16px; color:gray;">(Classical Image Processing)</span></h1>

<p>
This project implements a <b>classical image processing–based system</b> to detect and highlight
<b>surface anomalies (possible damage)</b> on rigid products using a single input image.
The application is built using <b>Python, OpenCV, and Flask</b> as part of an
<b>Image Processing academic assignment</b> and is intended for learning and demonstration purposes.
</p>

<hr/>

<h2>✨ Features</h2>
<ul>
  <li>Single image upload via Flask web interface</li>
  <li>Automatic product region isolation using contour detection</li>
  <li>Edge-based damage highlighting</li>
  <li>Morphological noise reduction</li>
  <li>Damage area estimation relative to product area</li>
  <li><b>ACCEPT / REJECT</b> condition output</li>
</ul>

<h2>🛠 Tech Stack</h2>
<ul>
  <li>Python</li>
  <li>OpenCV</li>
  <li>NumPy</li>
  <li>Flask</li>
</ul>

<h2>📁 Project Structure</h2>
<pre style="background:#f4f4f4; padding:10px; border-radius:5px;">
IP/
├── README.md
└── project/
    ├── app.py
    ├── main.py
    └── templates/
        └── index.html
</pre>

<h2>▶️ Setup & Run</h2>

<b>Step 1: Clone the repository</b>
<pre style="background:#f4f4f4; padding:10px; border-radius:5px;">
git clone https://github.com/karunrajkumar16/Product-Damage-Detection-using-Classical-Image-Processing.git
</pre>

<b>Step 2: Move into the project directory</b>
<pre style="background:#f4f4f4; padding:10px; border-radius:5px;">
cd Product-Damage-Detection-using-Classical-Image-Processing
</pre>

<b>Step 3: Install required dependencies</b>
<pre style="background:#f4f4f4; padding:10px; border-radius:5px;">
pip install -r requirements.txt
</pre>

<p><i>This installs all required Python libraries listed in <code>requirements.txt</code>.</i></p>

<b>Step 4: Run the application</b>
<pre style="background:#f4f4f4; padding:10px; border-radius:5px;">
python project/app.py
</pre>

<p>
Open your browser and visit:<br/>
<b>http://127.0.0.1:5000/</b>
</p>

<h2>⚙️ How It Works</h2>
<ul>
  <li>The input image is converted to grayscale and blurred</li>
  <li>Edges are detected using Canny edge detection</li>
  <li>Morphological operations are applied to reduce noise</li>
  <li>The largest contour is extracted as the product region</li>
  <li>Damage regions are highlighted and evaluated</li>
</ul>

<h2>⚠️ Limitations</h2>
<ul>
  <li>Sensitive to lighting variations</li>
  <li>Edge-based detection may flag textures or logos as damage</li>
  <li>Uses fixed thresholding</li>
  <li>Not suitable for production use</li>
</ul>

<h2>🚀 Deployment</h2>
<p>
This application is tested and deployed <b>locally</b> using Flask.
</p>

<h2>📄 License</h2>
<p>
MIT License
</p>

</div>
