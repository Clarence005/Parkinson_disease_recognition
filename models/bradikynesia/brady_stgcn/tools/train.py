import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import yaml
import os
import sys
from sklearn.metrics import classification_report
from collections import Counter
import random
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.feeder import Feeder
from model.stgcn import STGCN


def get_args():
    parser = argparse.ArgumentParser(description='Train ST-GCN on custom dataset')
    parser.add_argument('--config', type=str, required=True, help='Path to config file')
    return parser.parse_args()


def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True


def train():
    args = get_args()
    config = load_config(args.config)
    set_seed(config.get('seed', 42))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load datasets
    train_dataset = Feeder(**config['train_feeder_args'])
    val_dataset = Feeder(**config['val_feeder_args'])

    print(" Training label counts:", Counter(train_dataset.label))

    train_loader = DataLoader(train_dataset, batch_size=config['batch_size'], shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=config['batch_size'], shuffle=False)

    # Model
    model = STGCN(in_channels=3, num_class=config['num_class']).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['learning_rate'])

    best_acc = 0
    train_losses = []
    val_accuracies = []

    for epoch in range(1, config['num_epoch'] + 1):
        model.train()
        running_loss = 0.0

        for data, label in train_loader:
            data = data.to(device)
            label = label.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(train_loader)
        train_losses.append(avg_loss)
        print(f'\n🌀 Epoch {epoch}/{config["num_epoch"]} | Train Loss: {avg_loss:.4f}')

        # Validation
        model.eval()
        correct = total = 0
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for data, label in val_loader:
                data = data.to(device)
                label = label.to(device)
                outputs = model(data)
                _, predicted = torch.max(outputs.data, 1)

                total += label.size(0)
                correct += (predicted == label).sum().item()

                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(label.cpu().numpy())

        acc = 100 * correct / total
        val_accuracies.append(acc)

        print(f" Validation Accuracy: {acc:.2f}%")
        print(" Predicted class distribution:", Counter(all_preds))
        print(" True class distribution:", Counter(all_labels))
        print(classification_report(all_labels, all_preds, digits=3))

        # Save best model
        if acc > best_acc:
            best_acc = acc
            model_path = config.get('save_path', 'best_model.pth')
            torch.save(model.state_dict(), model_path)
            print(f"Best model saved at epoch {epoch}: {model_path}")

    # Plotting
    plt.figure()
    plt.plot(range(1, len(train_losses)+1), train_losses, label='Train Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Epochs')
    plt.legend()
    plt.grid()
    plt.savefig('train_loss.png')
    plt.close()

    plt.figure()
    plt.plot(range(1, len(val_accuracies)+1), val_accuracies, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Validation Accuracy Over Epochs')
    plt.legend()
    plt.grid()
    plt.savefig('val_accuracy.png')
    plt.close()

    print("Plots saved: train_loss.png & val_accuracy.png")


if __name__ == '__main__':
    train()
