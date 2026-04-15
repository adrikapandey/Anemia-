import os
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
            # Save the file locally
            file.save(filepath)
            
            # Predict using our inference module
            predicted_class, probability = predict_image(filepath)
            
            # Clean up the file after prediction
            if os.path.exists(filepath):
                os.remove(filepath)
                
            return jsonify({
                'prediction': predicted_class,
                'probability': round(probability * 100, 2)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
