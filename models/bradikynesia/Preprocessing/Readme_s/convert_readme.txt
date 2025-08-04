This script converts hand movement videos into a format compatible with the ST-GCN model for action classification. Here's what it does:

1) Reads hand-tapping videos from a folder (.avi files).

2  )Reads labels from a text file (right_hand_label.txt) that maps each video name to a class label (0–3).

3)Uses MediaPipe to detect the right-hand keypoints (21 landmarks) in each frame of each video.

4) Stores keypoint coordinates and confidence scores for each frame.

5 ) Saves this data in JSON files, where each JSON file represents one video and is formatted in the ST-GCN skeleton format.

6) Creates a label.pkl file, which contains a list of video names (without extension) and their corresponding labels. This file is used for training the model.