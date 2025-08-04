import os
import pickle
import numpy as np
import json
import torch
from torch.utils.data import Dataset

class Feeder(Dataset):
    def __init__(self, data_path, label_path, num_frame=150, num_joint=21, max_body=1):
        self.data_path = data_path
        self.label_path = label_path
        self.num_frame = num_frame
        self.num_joint = num_joint
        self.max_body = max_body

        with open(label_path, 'rb') as f:
            self.sample_name, self.label = pickle.load(f)

    def __len__(self):
        return len(self.sample_name)

    def __getitem__(self, index):
        name = self.sample_name[index]
        label = self.label[index]

        data = np.zeros((3, self.num_frame, self.num_joint, self.max_body), dtype=np.float32)

        # Load the JSON
        with open(os.path.join(self.data_path, name + '.json')) as f:
            json_data = json.load(f)

        frames = json_data['data']

        for i, frame in enumerate(frames[:self.num_frame]):
            if 'skeleton' in frame and frame['skeleton']:
                skeleton = frame['skeleton'][0]  # Only one person
                pose = skeleton['pose']         # [x1, y1, x2, y2, ..., x21, y21]
                if len(pose) != self.num_joint * 2:
                    continue  # skip malformed frames

                # Fill data: shape (3, T, V, M)
                for j in range(self.num_joint):
                    data[0, i, j, 0] = pose[2 * j]     # x
                    data[1, i, j, 0] = pose[2 * j + 1] # y
                    data[2, i, j, 0] = 1.0             # confidence (default 1)

        return torch.tensor(data, dtype=torch.float32), torch.tensor(label, dtype=torch.long)
