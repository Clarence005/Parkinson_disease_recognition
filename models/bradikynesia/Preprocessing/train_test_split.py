import os
import shutil
import pickle
import json
import random
from collections import defaultdict

# Constants
BASE_DIR = 'preprocessing'
SOURCE_DIR = os.path.join(BASE_DIR, 'augmented_skeletons')
TRAIN_DIR = os.path.join(BASE_DIR, 'train_videos')
VAL_DIR = os.path.join(BASE_DIR, 'val_videos')
LABEL_PKL = os.path.join(BASE_DIR, 'augment_label.pkl')
SPLIT_RATIO = 0.8  # 80% train, 20% validation

# Set seed for reproducibility (optional)
random.seed(42)

# Create output folders if not present
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)

# Step 1: Rebuild label.pkl from all JSONs
sample_names = []
sample_labels = []

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith('.json'):
        filepath = os.path.join(SOURCE_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            label = data.get("label")

        if label is not None:
            name = os.path.splitext(filename)[0]
            sample_names.append(name)
            sample_labels.append(int(label))  # ensure it's int
        else:
            print(f"⚠️ No label in {filename}")

# Save label.pkl for entire dataset
with open(LABEL_PKL, 'wb') as f:
    pickle.dump((sample_names, sample_labels), f)

print(f"\n Rebuilt label.pkl with {len(sample_names)} total samples.")

# Step 2: Group by class
class_samples = defaultdict(list)
for name, label in zip(sample_names, sample_labels):
    class_samples[label].append(name)

# Step 3: Create train/val split per class
train_samples, val_samples = [], []

for label, samples in class_samples.items():
    random.shuffle(samples)
    split_idx = int(len(samples) * SPLIT_RATIO)
    train = samples[:split_idx]
    val = samples[split_idx:]

    train_samples.extend([(name, label) for name in train])
    val_samples.extend([(name, label) for name in val])

print(f"\n Class-wise splitting done:")
for label in sorted(class_samples.keys()):
    print(f"  Class {label}: {len(class_samples[label])} → Train: {int(len(class_samples[label])*SPLIT_RATIO)} | Val: {len(class_samples[label]) - int(len(class_samples[label])*SPLIT_RATIO)}")

# Step 4: Move files and save new labels
def move_and_save(split_list, target_dir, pkl_path):
    names, labels = [], []
    for name, label in split_list:
        src = os.path.join(SOURCE_DIR, f"{name}.json")
        dst = os.path.join(target_dir, f"{name}.json")

        if os.path.exists(src):
            shutil.copyfile(src, dst)
            names.append(name)
            labels.append(label)
        else:
            print(f" Missing file: {src}")

    with open(pkl_path, 'wb') as f:
        pickle.dump((names, labels), f)

move_and_save(train_samples, TRAIN_DIR, os.path.join(BASE_DIR, 'train_label.pkl'))
move_and_save(val_samples, VAL_DIR, os.path.join(BASE_DIR, 'val_label.pkl'))

print("\nDataset split complete.")
print(f"Train samples: {len(train_samples)}")
print(f"Validation samples: {len(val_samples)}")
