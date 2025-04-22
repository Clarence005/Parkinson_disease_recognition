🧠 Parkinson's Disease Detection using Swin Transformer
This project focuses on the early detection of Parkinson's Disease using deep learning techniques, specifically leveraging the Swin Transformer architecture for robust feature extraction and classification. Parkinson’s is a progressive neurological disorder that impacts movement, and early diagnosis can significantly improve quality of life.

🔍 Project Overview
We use a vision-based deep learning approach to classify Parkinson's patients using hand-drawn spiral images or other motor-task-based visuals. The core model is based on Swin Transformer, a powerful and efficient vision transformer model that enables hierarchical representation learning through shifted windows. It outperforms conventional CNNs and vanilla ViTs on a variety of visual recognition tasks.

Key Highlights:

🔬 Swin Transformer Backbone: For precise and hierarchical feature extraction.

🧪 High Accuracy: Achieves excellent results on Parkinson's datasets for binary classification (Parkinson’s vs. Healthy).

📊 Performance Visualization: Includes training graphs, confusion matrix, and evaluation metrics like accuracy, precision, recall, and F1-score.

📱 Mobile App Integration
Alongside the model, we have built a cross-platform mobile application that allows users to:

Upload spiral drawings or motion task images.

Receive predictions instantly using the deployed Swin Transformer model.

View diagnostic feedback with a user-friendly interface.

Maintain history logs of previous predictions.

The app aims to assist healthcare providers and caregivers in non-invasively screening for Parkinson’s symptoms using digital drawing inputs.

🛠️ Tech Stack
Model: Swin Transformer (PyTorch / TensorFlow)

Dataset: Spiral drawing images (Parkinson’s dataset)

App: Flutter 

Backend: Flask

