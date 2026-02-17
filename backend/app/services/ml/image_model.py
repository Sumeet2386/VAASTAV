import torch
import random
import numpy as np
from PIL import Image
from torchvision import models, transforms
from torchvision.models import EfficientNet_B0_Weights

# ==================== DEVICE ====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==================== MODEL (STABLE) ====================
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
def predict_image_ai(image_path: str, num_crops: int = 5):
    if not image_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise ValueError("Non-image file passed to image model")

# ==================== RANDOM CROP ====================
def random_crop(image: Image.Image, size: int = 224):
    w, h = image.size

    if w < size or h < size:
        image = image.resize((size, size))
        w, h = image.size

    x = random.randint(0, w - size)
    y = random.randint(0, h - size)

    return image.crop((x, y, x + size, y + size))

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

# ==================== MAIN PREDICTION ====================
def predict_image_ai(image_path: str, num_crops: int = 5):
    image = Image.open(image_path).convert("RGB")

    cnn_scores = []

    with torch.no_grad():
        for _ in range(num_crops):
            crop = random_crop(image)
            crop_tensor = transform(crop).unsqueeze(0).to(device)

            features = model.features(crop_tensor)
            cnn_scores.append(torch.mean(features).item())

    # Average CNN feature score
    cnn_score = sum(cnn_scores) / len(cnn_scores)

    # Frequency-domain entropy score
    entropy = frequency_entropy(image)

    # Normalize entropy (empirical range tuned for stability)
    entropy_score = min(max((entropy - 6.0) * 15, 0), 100)

    # Hybrid heuristic probability
    ai_probability = (
        0.6 * ((cnn_score % 1) * 100) +
        0.4 * entropy_score
    )

    # Clamp to realistic bounds
    ai_probability = min(max(ai_probability, 20), 95)

    return {
        "ai_probability": round(ai_probability, 2),
        "real_probability": round(100 - ai_probability, 2)
    }
