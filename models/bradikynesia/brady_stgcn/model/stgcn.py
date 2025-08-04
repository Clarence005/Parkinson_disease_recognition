import torch
import torch.nn as nn
import numpy as np

class Graph:
    def __init__(self, layout='openpose', strategy='uniform'):
        self.num_node = 21
        self.edge = self._get_edge()
        self.A = self._get_adjacency(strategy)

    def _get_edge(self):
        self_link = [(i, i) for i in range(21)]
        neighbor_link = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (0, 9), (9, 10), (10, 11), (11, 12),
            (0, 13), (13, 14), (14, 15), (15, 16),
            (0, 17), (17, 18), (18, 19), (19, 20)
        ]
        return self_link + neighbor_link

    def _get_adjacency(self, strategy):
        A = np.zeros((self.num_node, self.num_node))
        for i, j in self.edge:
            A[i][j] = 1
            A[j][i] = 1
        normalize = lambda A: A / (A.sum(axis=0, keepdims=True) + 1e-6)
        return normalize(A)[np.newaxis, :, :]


class STGCNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, A, stride=1, residual=True):
        super().__init__()
        self.A = A
        self.gcn = nn.Conv2d(in_channels, out_channels, kernel_size=(1, 1))

        self.tcn = nn.Sequential(
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=(9, 1), stride=(stride, 1), padding=(4, 0)),
            nn.BatchNorm2d(out_channels)
        )

        if not residual:
            self.residual = lambda x: 0
        elif in_channels == out_channels and stride == 1:
            self.residual = lambda x: x
        else:
            self.residual = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=(stride, 1)),
                nn.BatchNorm2d(out_channels)
            )

        self.relu = nn.ReLU(inplace=True)

    def forward(self, x, A):
        # x: [N, C, T, V]
        N, C, T, V = x.size()
        y = torch.einsum('nctv,vw->nctw', x, A[0])  # Spatial GCN
        y = self.gcn(y)
        y = self.tcn(y)
        y = y + self.residual(x)
        y = self.relu(y)
        return y


class STGCN(nn.Module):
    def __init__(self, in_channels=3, num_class=4):
        super().__init__()
        graph = Graph()
        self.A = torch.tensor(graph.A, dtype=torch.float32, requires_grad=False)
        self.data_bn = nn.BatchNorm1d(in_channels * 21)

        self.layers = nn.ModuleList([
            STGCNBlock(in_channels, 64, self.A),
            STGCNBlock(64, 64, self.A),
            STGCNBlock(64, 128, self.A, stride=2),
            STGCNBlock(128, 256, self.A, stride=2)
        ])

        self.fc = nn.Linear(256, num_class)

    def forward(self, x):
        # x: [N, C, T, V, M]
        N, C, T, V, M = x.size()
        x = x.permute(0, 4, 3, 1, 2).contiguous().view(N * M, V * C, T)
        x = self.data_bn(x)
        x = x.view(N, M, V, C, T).permute(0, 1, 3, 4, 2).contiguous().view(N * M, C, T, V)

        for layer in self.layers:
            x = layer(x, self.A.to(x.device))

        x = x.mean(dim=[2, 3])  # Global average pooling
        x = self.fc(x)
        return x.view(N, M, -1).mean(dim=1)
