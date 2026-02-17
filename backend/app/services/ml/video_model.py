import cv2
import torch
import numpy as np
import random
from PIL import Image
from torchvision import models, transforms
from torchvision.models import EfficientNet_B0_Weights

# ==================== DEVICE ====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==================== MODEL ====================
weights = EfficientNet_B0_Weights.DEFAULT
model = models.efficientnet_b0(weights=weights)
model = model.to(device)
model.eval()

# ==================== TRANSFORMS ====================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ==================== FREQUENCY ENTROPY ====================
def frequency_entropy(image: Image.Image):
    gray = image.convert("L")
    img = np.array(gray)

    fft = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)

    magnitude = magnitude / (np.sum(magnitude) + 1e-8)
    magnitude = magnitude[magnitude > 0]

    entropy = -np.sum(magnitude * np.log2(magnitude))
    return entropy

# ==================== FRAME EXTRACTION ====================
def extract_frames(video_path, frame_interval=30, max_frames=10):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame_rgb))

            if len(frames) >= max_frames:
                break

        count += 1

    cap.release()
    return frames

# ==================== MAIN VIDEO PREDICTION ====================
def predict_video_ai(video_path: str):
    frames = extract_frames(video_path)

    if not frames:
        return {
            "ai_probability": 50.0,
            "real_probability": 50.0
        }

    cnn_scores = []
    entropy_scores = []

    with torch.no_grad():
        for frame in frames:
            tensor = transform(frame).unsqueeze(0).to(device)
            features = model.features(tensor)
            cnn_scores.append(torch.mean(features).item())

            entropy_scores.append(frequency_entropy(frame))

    # Average CNN score
    cnn_score = sum(cnn_scores) / len(cnn_scores)

    # Average entropy score
    entropy_avg = sum(entropy_scores) / len(entropy_scores)
    entropy_score = min(max((entropy_avg - 6.0) * 15, 0), 100)

    # Hybrid heuristic probability
    ai_probability = (
        0.6 * ((cnn_score % 1) * 100) +
        0.4 * entropy_score
    )

    ai_probability = min(max(ai_probability, 25), 95)

    return {
        "ai_probability": round(ai_probability, 2),
        "real_probability": round(100 - ai_probability, 2)
    }
