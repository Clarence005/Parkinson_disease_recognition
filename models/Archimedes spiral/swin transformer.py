import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from transformers import SwinForImageClassification, SwinConfig, AutoImageProcessor, get_scheduler
from torch.optim import AdamW
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm

# === CONFIG ===
DATA_DIR = 'spiral'
BATCH_SIZE = 16
NUM_EPOCHS = 20
NUM_CLASSES = 2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_NAME = "microsoft/swin-tiny-patch4-window7-224"
IMAGE_SIZE = 224
SAVE_PATH = "best_swin_model.pt"

# === Transforms ===
image_processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
normalize = transforms.Normalize(mean=image_processor.image_mean, std=image_processor.image_std)

train_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    normalize,
])

val_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    normalize,
])

# === Dataset & Dataloaders ===
train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, 'training'), transform=train_transforms)
val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, 'testing'), transform=val_transforms)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# === Model Setup ===
config = SwinConfig.from_pretrained(MODEL_NAME)
config.num_labels = NUM_CLASSES  # Important for initializing the classifier correctly
model = SwinForImageClassification.from_pretrained(MODEL_NAME, config=config, ignore_mismatched_sizes=True)
model.to(DEVICE)

# === Optimizer & Scheduler ===
optimizer = AdamW(model.parameters(), lr=5e-5)
lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=len(train_loader)*NUM_EPOCHS)

# === Training ===
best_val_acc = 0.0

for epoch in range(NUM_EPOCHS):
    model.train()
    total_loss = 0
    correct = 0

    for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS}"):
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(pixel_values=images)
        loss = nn.CrossEntropyLoss()(outputs.logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        total_loss += loss.item()
        preds = torch.argmax(outputs.logits, dim=1)
        correct += (preds == labels).sum().item()

    train_acc = correct / len(train_dataset)
    print(f"\nTrain Loss: {total_loss:.4f}, Train Accuracy: {train_acc*100:.2f}%")

    # === Validation ===
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(pixel_values=images)
            preds = torch.argmax(outputs.logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    val_acc = sum([p == t for p, t in zip(all_preds, all_labels)]) / len(all_labels)
    print("\nValidation Results:")
    print(f"Validation Accuracy: {val_acc*100:.2f}%")
    print(confusion_matrix(all_labels, all_preds))
    print(classification_report(all_labels, all_preds, target_names=train_dataset.classes))

    # === Save Best Model ===
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), SAVE_PATH)
        print(f"✅ Saved Best Model (Val Acc: {val_acc*100:.2f}%)")
