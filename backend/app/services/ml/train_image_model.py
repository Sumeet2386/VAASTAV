import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.efficientnet_b0(pretrained=True)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 1)

for param in model.parameters():
    param.requires_grad = False

model.classifier[1].requires_grad = True
model.to(device)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder("dataset", transform=transform)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.classifier[1].parameters(), lr=0.001)

for epoch in range(5):
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.float().to(device)
        optimizer.zero_grad()
        outputs = model(imgs).squeeze()
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

torch.save(model.state_dict(), "ai_detector.pth")
print("Training complete")

model.load_state_dict(torch.load("ai_detector.pth", map_location=device))
model.eval()
