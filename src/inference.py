import os
import numpy as np
import tensorflow as tf
from PIL import Image

MODEL_PATH = 'best_anemia_cnn_model.keras'

# Initialize model variable
model = None

def load_anemia_model():
    """Loads the Keras model if it exists."""
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Successfully loaded model weights.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}. Using mock predictions for UI testing.")

def predict_image(image_path):
    """
    Takes an image, resizes it to 256x256, converts to array, normalizes, 
    and predicts the presence of Anemia.
    """
    if model is None:
        # Development fallback if model isn't trained yet
        import random
        mock_prob = random.uniform(0, 1)
        return "Anemic" if mock_prob > 0.5 else "Non-Anemic", mock_prob

    try:
        # Load and resize image to match training specification
        img = Image.open(image_path).convert('RGB')
        img = img.resize((256, 256))
        
        # Convert to numpy array and normalize
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        # Make Prediction
        prediction_prob = float(model.predict(img_array)[0][0])
        
        # Binary Classification logic
        predicted_class = "Anemic" if prediction_prob > 0.5 else "Non-Anemic"
        return predicted_class, prediction_prob
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error", 0.0
