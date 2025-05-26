import io
import librosa
import joblib
import numpy as np
from fastapi import HTTPException
from fastapi import UploadFile
from typing import Dict, Any
from app.config.config import settings

async def predicated_class(mp3_file: UploadFile) -> Dict[str, Any]:
    contents = await mp3_file.read()
    features = extract_features_from_bytes(contents)
    
    if features is None:
        raise HTTPException(status_code=400, detail="Could not process audio file")
        
    features = features.reshape(1, -1)
    clf = joblib.load('app/source/age_classifier.pkl')
    predicted_class = clf.predict(features)[0]
    
    return {"predicted_class": predicted_class}

def extract_features_from_bytes(audio_bytes: bytes) -> np.ndarray:
    try:
        with io.BytesIO(audio_bytes) as audio_file:
            y, sr = librosa.load(audio_file, sr=None)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None