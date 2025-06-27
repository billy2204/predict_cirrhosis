import os
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

# --- Cấu hình đường dẫn gốc ---
ROOT_DIR = Path(r"C:\Users\Billy\Downloads\CirrMRI600+\Cirrhosis_T2_2D\Cirrhosis_T2_2D")  # thư mục gốc chứa train/test/valid
OUTPUT_DIR = Path(r"C:\Users\Billy\OneDrive\Documents\project_BME\yolo_dataset")   # nơi xuất dataset YOLO
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Các split
SPLITS = ["train", "valid", "test"]
# Tên lớp (ở đây chỉ 1 lớp: bất thường gan)
NAMES = ["abnormal_liver"]

# Tạo cấu trúc folder cho YOLO
for split in SPLITS:
    (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

# Hàm tính bounding box từ mask
def mask_to_yolo_boxes(mask_path):
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    h, w = mask.shape
    ys, xs = np.where(mask > 0)
    if ys.size == 0:
        return []
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    box_w = x_max - x_min
    box_h = y_max - y_min
    x_center = x_min + box_w / 2
    y_center = y_min + box_h / 2
    x_c = x_center / w
    y_c = y_center / h
    bw = box_w / w
    bh = box_h / h
    return [(0, x_c, y_c, bw, bh)]

# Xử lý với báo tiến trình
for split in SPLITS:
    src_split = ROOT_DIR / split
    if not src_split.exists():
        raise FileNotFoundError(f"Không tìm thấy thư mục: {src_split}")
    vols = [d for d in src_split.iterdir() if d.is_dir()]
    print(f"Processing split '{split}' with {len(vols)} volumes...")
    for vol in tqdm(vols, desc=f"Volumes ({split})"):
        img_dir = vol / "images"
        mask_dir = vol / "masks"
        img_files = list(img_dir.glob("*.png"))
        for img_path in tqdm(img_files, desc=f"Slices ({vol.name})", leave=False):
            name = img_path.stem
            mask_path = mask_dir / f"{name}.png"
            # copy ảnh sang thư mục mới
            dst_img = OUTPUT_DIR / "images" / split / f"{vol.name}_{name}.png"
            cv2.imwrite(str(dst_img), cv2.imread(str(img_path)))
            # tính bbox và ghi label
            boxes = mask_to_yolo_boxes(mask_path) if mask_path.exists() else []
            dst_lbl = OUTPUT_DIR / "labels" / split / f"{vol.name}_{name}.txt"
            with open(dst_lbl, 'w') as f:
                for cls, x_c, y_c, bw, bh in boxes:
                    f.write(f"{cls} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
print("🎉 Đã chuyển đổi xong dataset sang định dạng YOLO tại:", OUTPUT_DIR)
