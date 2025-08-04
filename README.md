🧠 Parkinson's Disease Detection using Swin Transformer & ST-GCN
This project focuses on the early detection of Parkinson's Disease using deep learning techniques, specifically leveraging the Swin Transformer for visual analysis and ST-GCN (Spatial-Temporal Graph Convolutional Network) for movement analysis. Parkinson’s is a progressive neurological disorder that impacts movement, and early diagnosis can significantly improve quality of life.

🔍 Project Overview
We employ a multi-modal approach combining image-based and motion-based analysis to classify Parkinson's patients:

Spiral Drawing Images: Classified using Swin Transformer, a powerful vision transformer model that enables hierarchical representation learning through shifted windows.

Bradykinesia Detection: Assessed using ST-GCN, which captures spatial and temporal dependencies from skeletal motion sequences to detect slowness of movement, a key symptom of Parkinson’s.

Key Highlights
🔬 Swin Transformer Backbone

Hierarchical visual feature extraction for spiral drawings and other motor-task images.

⚡ ST-GCN for Bradykinesia

Uses skeleton-based action recognition to identify slowness and reduced amplitude in movement sequences.

Analyzes temporal motion data from digital pen strokes or wearable sensors.

🧪 High Accuracy

Achieves robust results on Parkinson’s datasets for both binary classification (Parkinson’s vs. Healthy) and bradykinesia severity detection.

📊 Performance Visualization

Includes training graphs, confusion matrix, and metrics such as accuracy, precision, recall, F1-score, and ROC-AUC for both Swin Transformer and ST-GCN modules.

📱 Mobile App Integration
A cross-platform Flutter application provides an accessible interface for patients, caregivers, and healthcare providers:

Upload spiral drawings or motion sequence videos.

Receive predictions instantly via the deployed Swin Transformer (images) and ST-GCN (motion data) models.

Get diagnostic feedback with severity levels for bradykinesia.

Maintain history logs of predictions for tracking symptom progression.

🛠️ Tech Stack
Model (Visual): Swin Transformer (PyTorch / TensorFlow)

Model (Motion): ST-GCN (PyTorch Geometric / TensorFlow GCN)

Dataset:

Spiral drawing images (Parkinson’s dataset)

Motion sequences / skeleton data for bradykinesia assessment

App: Flutter

Backend: Flask (for API and model serving)

👉 This hybrid system strengthens Parkinson’s screening by combining drawing-based biomarkers with motion-based analysis, making detection more reliable and clinically useful.

