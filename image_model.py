"""
Image Model — MobileNetV2 inference for crop disease classification.
Extracted from the original app.py to be reusable across the application.
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os


def load_model():
    """Load the trained MobileNetV2 model and class names."""
    if not os.path.exists("classes.txt"):
        return None, None
    with open("classes.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    num_classes = len(class_names)

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)

    if os.path.exists("crop_disease_model.pth"):
        model.load_state_dict(
            torch.load("crop_disease_model.pth", map_location=torch.device("cpu"))
        )
    else:
        return None, class_names

    model.eval()
    return model, class_names


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """Preprocess a PIL image for MobileNetV2 inference."""
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)


def predict(model, class_names, image: Image.Image) -> dict:
    """
    Run inference on an image and return prediction results.

    Returns:
        dict with keys:
            - predicted_class: str
            - confidence: float (0-100)
            - top3: list of (class_name, probability) tuples
            - all_probabilities: tensor of all class probabilities
    """
    input_tensor = preprocess_image(image)

    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)

    predicted_class = class_names[predicted_idx.item()]
    confidence_score = confidence.item() * 100

    # Top 3 predictions
    top3_prob, top3_idx = torch.topk(probabilities, 3)
    top3 = [
        {"class": class_names[top3_idx[i].item()], "probability": round(top3_prob[i].item() * 100, 2)}
        for i in range(3)
    ]

    return {
        "predicted_class": predicted_class,
        "confidence": round(confidence_score, 2),
        "top3": top3,
    }
