import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# You can keep this in a separate file like 'styles.py' and import it
ADWAITA_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
}

QPushButton {
    background-color: #353535;
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
    border: 1px solid #101010;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #404040;
}

QPushButton:pressed {
    background-color: #2a2a2a;
}

QPushButton#suggested-action {
    background-color: #3584e4; /* Adwaita Blue */
    font-weight: bold;
}
"""

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adwaita-ish App")
        
        layout = QVBoxLayout()
        
        btn1 = QPushButton("Standard Button")
        
        btn2 = QPushButton("Suggested Action")
        btn2.setObjectName("suggested-action") # Match the CSS ID selector
        
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set the embedded style here
    app.setStyleSheet(ADWAITA_STYLE)
    
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
