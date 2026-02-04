from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MasterLoginWidget(QWidget):
    def __init__(self, on_success):
        super(MasterLoginWidget, self).__init__()
        self.on_success = on_success

        #self.setWindowTitle("Super Duper Secret")
        

        # Central Widget
        #central_widget = QWidget()
        #self.setCentralWidget(central_widget)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # UI Elements
        self.logo_label = QLabel()
        pixmap = QPixmap("assets/main-icon-blue.png")
        scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        self.label = QLabel("<h2>Enter Master Password</h2>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Unlock")
        self.login_button.clicked.connect(self.clicked_unlock)

        # Add to layout
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

    def clicked_unlock(self):
        # Get entered password with: self.password_input.text()
        
        self.on_success()