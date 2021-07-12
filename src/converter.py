import cv2
import base64
import numpy as np

def img_to_base64(image):             
    return base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()

def base64_to_img(jpg_as_text):
    jpg_original = base64.b64decode(jpg_as_text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    return cv2.imdecode(jpg_as_np, flags=1)