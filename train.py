import os
from ultralytics import YOLO

# Đường dẫn tới best model đã lưu
best_model_path = "best.pt"
print(f"Loading model from: {best_model_path}")

# Tiếp tục train từ best model
model = YOLO(best_model_path)
results = model.train(
    data="C:/Users/Billy/OneDrive/Documents/project_BME/yolo_dataset/data.yaml",
    epochs=20,
    imgsz=320,
    batch=2,
    device='cpu',
    project='training_results',
    name='exp1',
    patience=10,              # EarlyStopping với patience=10 epochs
    save=True,                 # lưu checkpoints, bao gồm best.pt
    verbose=True, 
    plots=True
)