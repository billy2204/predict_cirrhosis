import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class DragDropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag and drop an image here")
        self.setStyleSheet("border: 2px dashed #aaa;")
        self.pixmap = None

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
        self.setWindowTitle("PyQt5")
        self.initUI()

    def initUI(self):
        # Label kéo thả ảnh bên trái
        self.input_label = DragDropLabel()
        self.input_label.setFixedSize(, 300)

        self.output_label = QLabel("Output Here)
        self.output_label.setFixedSize(300, 300)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("border: 1px solid black;")

        # Nút xem output ở giữa
        self.btn_view_output = QPushButton("Xem Output")
        self.btn_view_output.setFixedSize(100, 40)
        self.btn_view_output.clicked.connect(self.show_output)

        # Layout ngang chính: input - nút - output
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_label)
        # Dùng layout dọc để căn giữa nút
        v_btn_layout = QVBoxLayout()
        v_btn_layout.addStretch()
        v_btn_layout.addWidget(self.btn_view_output, alignment=Qt.AlignCenter)
        v_btn_layout.addStretch()
        h_layout.addLayout(v_btn_layout)
        h_layout.addWidget(self.output_label)

        self.setLayout(h_layout)
        self.resize(750, 350)

    def show_output(self):
        # Hàm xem output
        if self.input_label.pixmap:
            self.output_label.setPixmap(self.input_label.pixmap.scaled(
                self.output_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.output_label.setText("")
        else:
            self.output_label.setText("Chưa có ảnh input")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
