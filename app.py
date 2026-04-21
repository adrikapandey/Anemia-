import os
import hashlib
import json
import redis
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.inference import load_anemia_model, predict_image

app = Flask(__name__)

# Configure upload physics
# We will temporarily save the image, process it, then delete it.
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Limit

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the AI model on server startup
load_anemia_model()

# Initialize external Redis Cache (Distributed Component)
redis_url = os.environ.get("REDIS_URL", None)
redis_client = None

if redis_url:
    try:
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        print("✅ Distributed Cache initialized: Connected to Redis successfully.")
    except Exception as e:
        print(f"⚠️  Warning: Failed to connect to Redis. Running without cache. Error: {e}")
        redis_client = None
else:
    print("ℹ️  No REDIS_URL environment variable found. Cache layer disabled by default.")

@app.route('/')
def index():
    """Renders the main frontend web page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API Endpoint to accept an image and return an Anemia prediction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file element in the request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # 1. Read bytes and Hash (Latency Cache Intercept)
            file_bytes = file.read()
            file_hash = hashlib.md5(file_bytes).hexdigest()
            file.seek(0) # Reset pointer so file.save() works properly

            # 2. Query Distributed Cache
            if redis_client:
                cached_result = redis_client.get(file_hash)
                if cached_result:
                    print(f"⚡️ CACHE HIT! Bypassing inference model for hash: {file_hash}")
                    data = json.loads(cached_result)
                    return jsonify({
                        'prediction': data['prediction'],
                        'probability': round(data['probability'] * 100, 2),
                        'cached': True
                    })

            # 3. Cache Miss: Normal Inference Flow
            file.save(filepath)
            predicted_class, probability = predict_image(filepath)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                
            # 4. Save to Cache
            if redis_client:
                r_payload = json.dumps({'prediction': predicted_class, 'probability': probability})
                redis_client.setex(file_hash, 86400, r_payload) # Cache for 24 hours

            return jsonify({
                'prediction': predicted_class,
                'probability': round(probability * 100, 2),
                'cached': False
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
