import base64, io, json, os
from pathlib import Path
import numpy as np
import cv2

try:
    import face_recognition
except Exception:
    face_recognition = None

UPLOAD_DIR = Path("uploads/faces")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def decode_base64_image(data_url: str):
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    img_bytes = base64.b64decode(data_url)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def image_to_embedding(image_bgr):
    if image_bgr is None:
        raise ValueError("Imagen inválida")
    if face_recognition is None:
        # Fallback técnico para ambientes sin dlib/face_recognition. No usar para producción biométrica.
        small = cv2.resize(image_bgr, (16, 8)).astype('float32').flatten() / 255.0
        if len(small) < 128:
            small = np.pad(small, (0, 128-len(small)))
        return small[:128].astype(float)
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model="hog")
    if not locations:
        raise ValueError("No se detectó rostro en la imagen")
    encodings = face_recognition.face_encodings(rgb, locations)
    if not encodings:
        raise ValueError("No se pudo generar embedding facial")
    return encodings[0].astype(float)

def save_face_image(estudiante_id: int, image_bgr):
    path = UPLOAD_DIR / f"student_{estudiante_id}.jpg"
    cv2.imwrite(str(path), image_bgr)
    return str(path).replace('\\','/')

def serialize_embedding(vec):
    return json.dumps([float(x) for x in vec])

def deserialize_embedding(text):
    return np.array(json.loads(text), dtype=float)

def compare_embeddings(candidate, known_embeddings, tolerance=0.48):
    best = None
    for item in known_embeddings:
        dist = float(np.linalg.norm(candidate - item['embedding']))
        confidence = max(0.0, min(1.0, 1.0 - dist)) if face_recognition is None else max(0.0, min(1.0, 1.0 - dist/0.75))
        if best is None or dist < best['distance']:
            best = {**item, 'distance': dist, 'confidence': confidence}
    if best and best['distance'] <= tolerance:
        return best
    return None
