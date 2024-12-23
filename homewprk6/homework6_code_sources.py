# -*- coding: utf-8 -*-
"""homework6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17mgJ3ghgUjn37oIxCt44QM8lyLXwxBKU
"""

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler

# Generate or load your dataset (replace make_regression with your actual housing data)
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

# Data preprocessing
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_train = scaler_X.fit_transform(X_train)
X_val = scaler_X.transform(X_val)
y_train = scaler_y.fit_transform(y_train.reshape(-1, 1))
y_val = scaler_y.transform(y_val.reshape(-1, 1))

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.float32).view(-1, 1)

# Define the model
class HousingSingleLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Train function
def train_single_layer_housing_model(X_train, y_train, X_val, y_val, learning_rate, epochs):
    input_dim = X_train.shape[1]
    hidden_dim = 8
    model = HousingSingleLayerModel(input_dim, hidden_dim)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    train_losses, val_losses = [], []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train)
        train_loss = loss_fn(predictions, y_train)
        train_loss.backward()
        optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            val_predictions = model(X_val)
            val_loss = loss_fn(val_predictions, y_val).item()

        if (epoch + 1) % 100 == 0:
            train_losses.append(train_loss.item())
            val_losses.append(val_loss)
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss.item():.4f}, Validation Loss: {val_loss:.4f}")

    print("Final Train Loss:", train_losses[-1])
    print("Final Validation Loss:", val_losses[-1])
    return model, train_losses, val_losses

# Train the model
single_layer_model, train_losses_1a, val_losses_1a = train_single_layer_housing_model(
    X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, learning_rate=0.05, epochs=1000
)

class HousingMultiLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dims):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.fc4 = nn.Linear(hidden_dims[2], 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.dropout(self.relu(self.fc3(x)))
        x = self.fc4(x)
        return x

def train_multi_layer_housing_model(X_train, y_train, X_val, y_val, learning_rate, epochs):
    input_dim = X_train.shape[1]
    hidden_dims = [64, 32, 16]
    model = HousingMultiLayerModel(input_dim, hidden_dims)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    train_losses, val_losses = [], []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train)
        train_loss = loss_fn(predictions, y_train)
        train_loss.backward()
        optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            val_predictions = model(X_val)
            val_loss = loss_fn(val_predictions, y_val).item()

        if (epoch + 1) % 100 == 0:
            train_losses.append(train_loss.item())
            val_losses.append(val_loss)
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss.item():.4f}, Validation Loss: {val_loss:.4f}")

    print("Final Train Loss:", train_losses[-1])
    print("Final Validation Loss:", val_losses[-1])
    return model, train_losses, val_losses

# Train the model
multi_layer_model, train_losses_1b, val_losses_1b = train_multi_layer_housing_model(
    X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, learning_rate=0.001, epochs=1000
)

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

# Load the cancer dataset
cancer_data = load_breast_cancer()
X = cancer_data.data
y = cancer_data.target

# Split and preprocess
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
scaler_X = StandardScaler()
X_train = scaler_X.fit_transform(X_train)
X_val = scaler_X.transform(X_val)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.float32).view(-1, 1)

# Define the single-hidden-layer model
class CancerSingleLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

# Train function
def train_single_layer_cancer_model(X_train, y_train, X_val, y_val, learning_rate, epochs):
    input_dim = X_train.shape[1]
    hidden_dim = 32
    model = CancerSingleLayerModel(input_dim, hidden_dim)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.BCELoss()  # Binary Cross-Entropy Loss
    train_losses, val_losses = [], []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train)
        train_loss = loss_fn(predictions, y_train)
        train_loss.backward()
        optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            val_predictions = model(X_val)
            val_loss = loss_fn(val_predictions, y_val).item()

        if (epoch + 1) % 100 == 0:
            train_losses.append(train_loss.item())
            val_losses.append(val_loss)
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss.item():.4f}, Validation Loss: {val_loss:.4f}")

    print("Final Train Loss:", train_losses[-1])
    print("Final Validation Loss:", val_losses[-1])
    return model, train_losses, val_losses

# Train the model
single_layer_cancer_model, train_losses_2a, val_losses_2a = train_single_layer_cancer_model(
    X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, learning_rate=0.001, epochs=1000
)

class CancerMultiLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dims):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.fc4 = nn.Linear(hidden_dims[2], 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.sigmoid(self.fc4(x))
        return x

# Train function
def train_multi_layer_cancer_model(X_train, y_train, X_val, y_val, learning_rate, epochs):
    input_dim = X_train.shape[1]
    hidden_dims = [64, 32, 16]
    model = CancerMultiLayerModel(input_dim, hidden_dims)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.BCELoss()
    train_losses, val_losses = [], []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train)
        train_loss = loss_fn(predictions, y_train)
        train_loss.backward()
        optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            val_predictions = model(X_val)
            val_loss = loss_fn(val_predictions, y_val).item()

        if (epoch + 1) % 100 == 0:
            train_losses.append(train_loss.item())
            val_losses.append(val_loss)
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss.item():.4f}, Validation Loss: {val_loss:.4f}")

    print("Final Train Loss:", train_losses[-1])
    print("Final Validation Loss:", val_losses[-1])
    return model, train_losses, val_losses

# Train the model
multi_layer_cancer_model, train_losses_2b, val_losses_2b = train_multi_layer_cancer_model(
    X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, learning_rate=0.001, epochs=1000
)

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Load CIFAR-10 dataset
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Define the model with one hidden layer of 256 nodes
class CIFARSingleLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten input
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Train function
def train_single_layer_cifar_model(train_loader, test_loader, learning_rate, epochs):
    input_dim = 32 * 32 * 3  # CIFAR-10 images are 32x32x3
    hidden_dim = 256
    output_dim = 10  # 10 classes
    model = CIFARSingleLayerModel(input_dim, hidden_dim, output_dim)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    train_losses, test_accuracies = [], []
    start_time = time.time()

    for epoch in range(epochs):
        # Training step
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # Validation step
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        train_losses.append(running_loss / len(train_loader))
        test_accuracies.append(100 * correct / total)

        print(f"Epoch {epoch+1}/{epochs}, Loss: {train_losses[-1]:.4f}, Accuracy: {test_accuracies[-1]:.2f}%")

    end_time = time.time()
    training_time = end_time - start_time
    return model, train_losses, test_accuracies, training_time

# Train the model
single_layer_model, train_losses_3a, test_accuracies_3a, training_time_3a = train_single_layer_cifar_model(
    train_loader, test_loader, learning_rate=0.01, epochs=100
)

# Display results
print("Problem 3a Results (Single Hidden Layer):")
print("Training Time:", training_time_3a, "seconds")
print("Train Losses (last epoch):", train_losses_3a[-1])
print("Test Accuracy:", test_accuracies_3a[-1], "%")

# Define the model with three hidden layers
class CIFARMultiLayerModel(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dims[0])
        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.fc3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.fc4 = nn.Linear(hidden_dims[2], output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten input
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x

# Train function for multi-layer network
def train_multi_layer_cifar_model(train_loader, test_loader, learning_rate, epochs):
    input_dim = 32 * 32 * 3
    hidden_dims = [512, 256, 128]  # Three hidden layers
    output_dim = 10
    model = CIFARMultiLayerModel(input_dim, hidden_dims, output_dim)
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    train_losses, test_accuracies = [], []
    start_time = time.time()

    for epoch in range(epochs):
        # Training step
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # Validation step
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        train_losses.append(running_loss / len(train_loader))
        test_accuracies.append(100 * correct / total)

        print(f"Epoch {epoch+1}/{epochs}, Loss: {train_losses[-1]:.4f}, Accuracy: {test_accuracies[-1]:.2f}%")

    end_time = time.time()
    training_time = end_time - start_time
    return model, train_losses, test_accuracies, training_time

# Train the model
multi_layer_model, train_losses_3b, test_accuracies_3b, training_time_3b = train_multi_layer_cifar_model(
    train_loader, test_loader, learning_rate=0.01, epochs=100
)

# Display results
print("Problem 3b Results (Three Hidden Layers):")
print("Training Time:", training_time_3b, "seconds")
print("Train Losses (last epoch):", train_losses_3b[-1])
print("Test Accuracy:", test_accuracies_3b[-1], "%")