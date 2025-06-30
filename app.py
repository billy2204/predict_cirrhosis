import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np
import cv2
from ultralytics import YOLO
from datetime import datetime

class DragDropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag and drop an image here")
        self.setStyleSheet("border: 2px dashed #aaa;")
        self.pixmap = None
        self.image_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.set_image(file_path)

    def set_image(self, file_path):
        self.image_path = file_path
        self.pixmap = QPixmap(file_path)
        if not self.pixmap.isNull():
            self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.setText("")

    def resizeEvent(self, event):
        if self.pixmap:
            self.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cirrhosis Detection App")
        self.model = YOLO("best.pt")
        self.initUI()

    def initUI(self):
        self.input_label = DragDropLabel()
        self.input_label.setFixedSize(300, 300)

        self.output_label = QLabel("Output Here")
        self.output_label.setFixedSize(300, 300)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("border: 1px solid black;")

        self.result_text = QLabel("")
        self.result_text.setAlignment(Qt.AlignCenter)

        self.btn_predict = QPushButton("Predict & Save Result")
        self.btn_predict.setFixedSize(180, 40)
        self.btn_predict.clicked.connect(self.predict_and_save)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_label)

        v_btn_layout = QVBoxLayout()
        v_btn_layout.addStretch()
        v_btn_layout.addWidget(self.btn_predict, alignment=Qt.AlignCenter)
        v_btn_layout.addStretch()
        h_layout.addLayout(v_btn_layout)

        h_layout.addWidget(self.output_label)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.result_text)

        self.setLayout(v_layout)
        self.resize(800, 420)

    def predict_and_save(self):
        image_path = self.input_label.image_path
        if not image_path:
            self.output_label.setText("Chưa có ảnh input")
            return

        results = self.model(image_path)
        result = results[0]

        if len(result.boxes) == 0:
            self.result_text.setText("✅ Healthy liver (no cirrhosis detected)")
            self.output_label.setPixmap(QPixmap(image_path).scaled(
                self.output_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.result_text.setText("⚠️ Cirrhotic liver detected")
            img_array = result.plot()
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.output_label.setPixmap(pixmap.scaled(
                self.output_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Save the result
            os.makedirs("results", exist_ok=True)
            filename = os.path.basename(image_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join("results", f"pred_{timestamp}_{filename}")
            cv2.imwrite(save_path, img_array)
            print(f"✅ Kết quả đã lưu tại: {save_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
