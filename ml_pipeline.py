import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, f1_score, accuracy_score
import numpy as np

def main():
    # Dataset paths
    BASE_DIR = 'Plant Village Dataset'
    TRAIN_DIR = os.path.join(BASE_DIR, 'Train')
    VAL_DIR = os.path.join(BASE_DIR, 'Val')
    TEST_DIR = os.path.join(BASE_DIR, 'Test')

    BATCH_SIZE = 32
    IMG_SIZE = 224

    print("Loading datasets with PyTorch...")
    
    # Transforms
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(IMG_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    val_test_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transform)
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_test_transform)
    test_dataset = datasets.ImageFolder(TEST_DIR, transform=val_test_transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    class_names = train_dataset.classes
    num_classes = len(class_names)
    print(f"Found {num_classes} classes.")

    # Device configuration
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load MobileNetV2
    print("Building MobileNetV2 model...")
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    # Freeze base layers
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace classifier
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

    # Train model
    EPOCHS = 2 # 2 epochs for a quick prototype
    print(f"Starting training for {EPOCHS} epochs...")
    
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            
        epoch_loss = running_loss / len(train_dataset)
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {epoch_loss:.4f}")
        
        # Validation
        model.eval()
        val_correct = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)
        
        val_acc = val_correct.float() / len(val_dataset)
        print(f"Validation Accuracy: {val_acc:.4f}")

    # Evaluation
    print("\nEvaluating on Test dataset...")
    model.eval()
    
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # Calculate Metrics
    accuracy = accuracy_score(all_labels, all_preds)
    f1 = f1_score(all_labels, all_preds, average='weighted')
    report = classification_report(all_labels, all_preds, target_names=class_names, zero_division=0)
    
    print(f'\nTest Accuracy: {accuracy:.4f}')
    print(f'Weighted F1 Score: {f1:.4f}')

    print("\nClassification Report:")
    print(report)

    # Save metrics to a separate file
    print("\nSaving metrics to metrics_output.txt...")
    with open("metrics_output.txt", "w") as f:
        f.write(f"Test Accuracy: {accuracy:.4f}\n")
        f.write(f"Weighted F1 Score: {f1:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)

    # Save the model and class names for Streamlit
    print("\nSaving the model...")
    torch.save(model.state_dict(), "crop_disease_model.pth")
    with open("classes.txt", "w") as f:
        f.write("\n".join(class_names))
    print("Model and classes saved.")

if __name__ == "__main__":
    main()
