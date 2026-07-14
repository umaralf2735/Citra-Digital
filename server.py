import os
import cv2
import numpy as np
from flask import Flask, request, send_file
from flask_cors import CORS
import io

import image_processor as ip

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return {"error": "Tidak ada gambar yang diunggah"}, 400
    
    file = request.files['image']
    action = request.form.get('action')
    param = request.form.get('param')
    
    # Read image from memory
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"error": "Format gambar tidak valid"}, 400

    # Apply the corresponding action
    try:
        if action == 'grayscale':
            img = ip.to_grayscale(img)
        elif action == 'invert':
            img = ip.invert(img)
        elif action == 'equalize':
            img = ip.histogram_equalization(img)
        elif action == 'filter':
            img = ip.apply_filter(img, param)
        elif action == 'edge':
            img = ip.edge_detection(img, param)
        elif action == 'creative':
            if param == 'cartoon': img = ip.cartoon_effect(img)
            elif param == 'sketch': img = ip.sketch_effect(img)
            elif param == 'sepia': img = ip.sepia_effect(img)
        elif action == 'transform':
            if param in ['cw', 'ccw']: img = ip.rotate_image(img, param)
            elif param in ['h', 'v']: img = ip.flip_image(img, param)
        elif action == 'advanced':
            if param == 'sharpen': img = ip.sharpen_effect(img)
            elif param == 'emboss': img = ip.emboss_effect(img)
            elif param == 'vignette': img = ip.vignette_effect(img)
            elif param == 'noise': img = ip.add_noise(img)
        elif action == 'brightness_contrast':
            b = int(request.form.get('brightness', 0))
            c = float(request.form.get('contrast', 1.0))
            img = ip.adjust_brightness_contrast(img, b, c)
    except Exception as e:
        return {"error": str(e)}, 500

    # Encode back to JPEG
    _, buffer = cv2.imencode('.jpg', img)
    out_io = io.BytesIO(buffer)
    out_io.seek(0)
    
    return send_file(out_io, mimetype='image/jpeg')

if __name__ == '__main__':
    print("🚀 Menjalankan Mini Photoshop Web Server di http://127.0.0.1:2026")
    app.run(debug=True, port=2026)
