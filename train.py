import os
from ultralytics import YOLO

# Load và train model với EarlyStopping thông qua tham số patience
model = YOLO("yolov8n.pt")
results = model.train(
    data="C:/Users/Billy/OneDrive/Documents/project_BME/yolo_dataset/data.yaml",
    epochs=10,
    imgsz=320,
    batch=4,
    device='cpu',
    project='training_results',
    name='exp1',
    patience=10,              # EarlyStopping với patience=10 epochs
    save=True                 # lưu checkpoints, bao gồm best.pt
    verbose=True, 
    plots=True
)

# Đường dẫn tới best model
best_model = results.best
print(f"Best model saved at: {best_model}")
