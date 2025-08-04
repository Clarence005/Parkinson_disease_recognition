import os
import cv2
import numpy as np
import mediapipe as mp
import json
import pickle
from tqdm import tqdm

# === PATHS AND SETUP ===

VIDEO_DIR = "preprocessing/righthand_videos"             # Folder containing right-hand videos (.avi)
LABEL_FILE = "preprocessing/right_hand_label.txt"         # Text file with labels: <video_name> <label>
OUTPUT_DIR = "preprocessing/output_skeletons"             # Folder to save the output .json skeletons
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Initialize MediaPipe Hand Detection ===

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)  # Real-time mode, single hand

# === Get List of Video Files ===

video_files = sorted([f for f in os.listdir(VIDEO_DIR) if f.endswith(".avi")])

# === Load Labels from Text File ===

labels = {}
with open(LABEL_FILE, 'r') as f:
    for line in f:
        vid, lbl = line.strip().split()
        labels[vid] = int(lbl)

# === Process Each Video File ===

for file_name in tqdm(video_files):
    video_path = os.path.join(VIDEO_DIR, file_name)
    cap = cv2.VideoCapture(video_path)
    frames = []  # To store keypoints of each frame
    scores = []  # To store confidence scores

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        result = hands.process(rgb)  # Get hand landmarks

        keypoints = np.zeros((21, 2))  # (x, y) for 21 landmarks
        conf = np.zeros(21)            # Confidence scores

        # If hand landmarks are detected
        if result.multi_hand_landmarks:
            for idx, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                keypoints[idx] = [lm.x * w, lm.y * h]  # Scale to original image
                conf[idx] = 1.0  # Set confidence score to 1.0 (since MediaPipe doesn't provide it)

            # Optional: Draw landmarks on frame for visualization
            mp_drawing.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

        # Append to lists
        frames.append(keypoints)
        scores.append(conf)

        # Display frame
        cv2.imshow("Hand Landmarks", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Press 'q' to exit early

    # === Convert to ST-GCN Compatible JSON Format ===

    data_list = []
    for idx in range(len(frames)):
        keypoints_flat = frames[idx].flatten().tolist()  # Flatten to 42 values: [x1, y1, ..., x21, y21]
        scores_flat = scores[idx].tolist()

        frame_data = {
            "frame_index": idx + 1,
            "skeleton": [{
                "pose": keypoints_flat,
                "score": scores_flat,
                "id": None
            }]
        }
        data_list.append(frame_data)

    json_data = {
        "data": data_list,
        "label": str(labels[file_name.replace('.avi', '')]),
        "label_index": labels[file_name.replace('.avi', '')]
    }

    # Save JSON
    json_path = os.path.join(OUTPUT_DIR, file_name.replace('.avi', '.json'))
    with open(json_path, 'w') as f:
        json.dump(json_data, f)

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()

# === Create label.pkl File ===

sample_names = [f.replace('.avi', '') for f in video_files]
sample_labels = [labels[name] for name in sample_names]
with open('label.pkl', 'wb') as f:
    pickle.dump((sample_names, sample_labels), f)

print("All videos converted to ST-GCN format. label.pkl created.")
