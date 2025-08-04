import os
import json
import random
import shutil
from collections import defaultdict
from tqdm import tqdm
import pickle
import numpy as np

INPUT_DIR = 'preprocessing/output_skeletons'         # original JSONs
OUTPUT_DIR = 'preprocessing/augmented_skeletons'     # augmented JSONs
TARGET_PER_CLASS = 112                               # desired samples per class
AUGMENT_NOISE_STD = 0.02                             # ~2% Gaussian jitter

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load and group files by label
label_to_files = defaultdict(list)
all_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json')]

for f in all_files:
    with open(os.path.join(INPUT_DIR, f)) as jf:
        data = json.load(jf)
        label = data.get('label')
        if label is not None:
            label_to_files[label].append(f)

print(" Original class counts:")
for label in sorted(label_to_files.keys(), key=int):
    print(f"  Class {label}: {len(label_to_files[label])} files")

# Copy originals & augment
new_label_list = []

for label, files in label_to_files.items():
    cur_count = len(files)
    shortfall = TARGET_PER_CLASS - cur_count

    # 1. Copy original files
    for f in files:
        src_path = os.path.join(INPUT_DIR, f)
        dst_path = os.path.join(OUTPUT_DIR, f)
        shutil.copyfile(src_path, dst_path)
        new_label_list.append((f.replace('.json', ''), int(label)))

    if shortfall <= 0:
        continue

    # 2. Create augmented files
    print(f" Augmenting {shortfall} samples for class {label}")
    for i in tqdm(range(shortfall)):
        src_file = random.choice(files)
        with open(os.path.join(INPUT_DIR, src_file)) as jf:
            data = json.load(jf)

        # Add Gaussian noise to pose keypoints
        for frame in data['data']:
            for person in frame.get('skeleton', []):
                pose = person.get('pose', [])
                if pose:
                    for j in range(len(pose)):
                        noise = random.gauss(0, AUGMENT_NOISE_STD)
                        pose[j] += noise

        # Create new filename
        new_filename = f"{os.path.splitext(src_file)[0]}_aug{i}.json"
        new_path = os.path.join(OUTPUT_DIR, new_filename)

        # Save new JSON
        with open(new_path, 'w') as out_f:
            json.dump(data, out_f)

        new_label_list.append((new_filename.replace('.json', ''), int(label)))

# Save label.pkl
label_pkl_path = os.path.join("preprocessing", 'augment_label.pkl')
with open(label_pkl_path, 'wb') as f:
    pickle.dump(new_label_list, f)

print("\n Augmentation complete!")
print(f" Augmented dataset saved to: {OUTPUT_DIR}")
print(f" label.pkl created with {len(new_label_list)} entries.")
