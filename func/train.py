import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import BindingAffinityPredictor
import esm
import pandas as pd

# 1. Config
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 8
EPOCHS = 10
LR = 1e-4

# 2. Dummy Dataset class
class BindingDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        scfv = self.data.iloc[idx]['scfv']
        antigen = self.data.iloc[idx]['antigen']
        label = self.data.iloc[idx]['affinity']
        return scfv, antigen, torch.tensor(label, dtype=torch.float32)

# 3. Load data
# CSV 파일은 세 column: "scfv", "antigen", "affinity"
df = pd.read_csv("data/binding_data.csv")
dataset = BindingDataset(df)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# 4. Load model
model = BindingAffinityPredictor().to(DEVICE)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.mlp.parameters(), lr=LR)  # MLP만 학습

# 5. Training loop
model.train()
for epoch in range(EPOCHS):
    total_loss = 0
    for scfv, antigen, labels in dataloader:
        scfv, antigen, labels = scfv, antigen, labels.to(DEVICE)

        preds = model(scfv, antigen)
        loss = criterion(preds.squeeze(), labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/len(dataloader):.4f}")

# 6. Save weights
# torch.save(model.mlp.state_dict(), "weights/mlp_weights.pth")
# 키 충동 그냥 mlp만 학습했으니.
torch.save({'mlp': model.mlp.state_dict()}, "mlp_weights.pth")
