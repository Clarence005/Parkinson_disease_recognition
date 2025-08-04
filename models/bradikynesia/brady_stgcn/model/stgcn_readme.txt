This repository contains a Spatio-Temporal Graph Convolutional Network (ST-GCN) designed for classifying Parkinson’s bradykinesia levels based on skeleton data extracted from finger tapping videos

1) This implementation consists of:

    #1) Graph Construction (Graph class)
    #2) ST-GCN Model Architecture (STGCN and STGCNBlock classes)
    #3) Pose Normalization and BatchNorm
    #4) Spatio-temporal Feature Learning
    #5) Classification Head

2)It processes input tensors shaped as [N, C, T, V, M] where:

    N = Batch size
    C = Number of input channels (typically 3: x, y, confidence)
    T = Number of frames
    V = Number of joints (21 in this case)
    M = Number of persons per frame (set to 1)

3) what is Graph class

    The Graph class defines the skeleton structure using 21 joints connected in a tree-like topology starting from the wrist.

    Key Points:
        #1) self_link: Self-loops for each node
        #2) neighbor_link: Anatomical connections (mimicking fingers from wrist)
        #3) Returns: Adjacency matrix A with uniform normalization
        0: wrist    
        1-4: thumb  
        5-8: index  
        9-12: middle  
        13-16: ring  
        17-20: pinky

4) What is STGCNBlock class

    #1) This block handles one layer of the ST-GCN architecture. Each block includes:
    #2) Graph Convolution (gcn) — learns spatial features over joints
    #3) Temporal Convolution (tcn) — learns motion patterns across time
    #4) Residual Connection — supports stable deep training
    #5) ReLU Activation — non-linearity for feature learning


5) What us STGCN Model 

    The STGCN model stacks multiple STGCNBlock layers to extract deep spatio-temporal features, followed by global average pooling and a fully connected layer for final classification.

    Input: [N, C, T, V, M]

    1. BatchNorm across input joints and channels
    2. 4 ST-GCN blocks:
    - Block1: 3 → 64
    - Block2: 64 → 64
    - Block3: 64 → 128 (stride=2, temporal downsampling)
    - Block4: 128 → 256 (stride=2, temporal downsampling)
    3. Global Average Pooling across T and V
    4. FC Layer (Fully connected layers) : 256 → 4 (classes)
    5. Output: Softmax class scores
    