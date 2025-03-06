import os
import logging
import numpy as np
import librosa
import librosa.display
import tensorflow as tf
import matplotlib.pyplot as plt
from datetime import datetime
from django.shortcuts import render,redirect
from django.core.files.storage import default_storage
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from .models import DiagnosticTest,user
from django.contrib.auth.decorators import login_required
from .generate_report import generate_report

# Initialize logging
logger = logging.getLogger(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'dlmodel/RDMS_cnn_model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Label Encoder for Disease Classes
encoder = LabelEncoder()
encoder.classes_ = np.array(["Asthma", "Bronchiectasis", "Bronchiolitis", "COPD",
                             "LRTI", "Pneumonia", "URTI", "Normal"])

def generate_spectrogram(file_path, save_path):
    """Generates and saves a spectrogram from an audio file."""
    try:
        sr_new = 16000  # Target sample rate
        x, sr = librosa.load(file_path, sr=sr_new)

        plt.figure(figsize=(8, 4))
        librosa.display.specshow(librosa.amplitude_to_db(librosa.stft(x), ref=np.max),
                                 sr=sr_new, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title("Spectrogram")
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    except Exception as e:
        logger.error(f"Error generating spectrogram: {e}")

def preprocess_audio(file_path):
    """Preprocesses the audio file into MFCC features."""
    try:
        sr_new = 16000  
        max_len = 5 * sr_new  

        x, sr = librosa.load(file_path, sr=sr_new)

        if x.shape[0] < max_len:
            x = np.pad(x, (0, max_len - x.shape[0]))
        else:
            x = x[:max_len]

        feature = librosa.feature.mfcc(y=x, sr=sr_new, n_mfcc=20)
        feature = np.expand_dims(feature, axis=-1)
        feature = np.expand_dims(feature, axis=0)

        return feature
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return None

def predict_disease(request):
    """Handles disease prediction from an uploaded audio file."""
    if request.method == 'POST' and request.FILES.get('audiofile'):
        audio_file = request.FILES['audiofile']
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"

        # Ensure temp directory exists
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        try:
            patient_name = request.POST.get('name', 'Unknown')
            age = request.POST.get('age', 'Unknown')
            symptoms = request.POST.get('symptoms', 'Not Provided')
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Generate spectrogram and store it in a static/media folder
            spectrogram_filename = f"{filename}_spectrogram.png"
            spectrogram_path = os.path.join(settings.MEDIA_ROOT, 'spectrograms', spectrogram_filename)
            os.makedirs(os.path.dirname(spectrogram_path), exist_ok=True)

            generate_spectrogram(file_path, spectrogram_path)

            # Convert file path to URL
            spectrogram_url = f"{settings.MEDIA_URL}spectrograms/{spectrogram_filename}"

            # Preprocess and Predict
            audio_features = preprocess_audio(file_path)
            if audio_features is None:
                raise ValueError("Failed to process the audio file.")

            prediction = model.predict(audio_features)
            predicted_class = np.argmax(prediction, axis=1)
            confidence = np.max(prediction) * 100
            predicted_label = encoder.inverse_transform(predicted_class)[0]

            # Determine severity
            severity = "Mild" if confidence < 60 else "Moderate" if confidence < 85 else "Severe"

            # Generate Report with Spectrogram
            report_filename = f"{patient_name.replace(' ', '_')}_report.pdf"
            report_path = generate_report(patient_name, age, symptoms, date, predicted_label, confidence, severity, spectrogram_path)

            # Get report URL
            report_url = f"{settings.MEDIA_URL}reports/{report_filename}"

            result = f"Disease: {predicted_label} ({confidence:.2f}% confidence), Severity: {severity}"

        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            result = f"Error: {str(e)}"
            report_url = None
            spectrogram_url = None

        finally:
            # Delete temporary files
            if os.path.exists(file_path):
                os.remove(file_path)

        return render(request, 'index.html', {
            'result': result,
            'report_path': report_url,
            'spectrogram_path': spectrogram_url
        })

    return render(request, 'index.html')







