from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QPushButton, 
    QLabel, 
    QStyle, 
    QHBoxLayout, 
    QToolButton, 
    QMenu,
    QDialog,
    QCheckBox,
    QComboBox,
    QStyleFactory,
    QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

import __init__

class StartupWidget(QWidget):
    def __init__(self, on_unlock, on_new, on_verify):
        super(StartupWidget, self).__init__()
        self.on_unlock = on_unlock
        self.on_new = on_new
        self.on_verify = on_verify

        # Central Widget
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Add layout for hamburger menu
        self.header_layout = QHBoxLayout()
        self.header_layout.addStretch() # Push menu button to the right
        # Hamburger menu button
        self.menu_button = QToolButton()
        self.menu_button.setText("Menu")
        self.menu_button.setFixedSize(70, 30) 
        self.hamburger_menu = QMenu(self)
        # Enable transparency so CSS rounded corners work
        self.hamburger_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Remove the native OS window frame that often forces square corners
        self.hamburger_menu.setWindowFlags(
            self.hamburger_menu.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint
        )  

        # Menu actions
        action_settings = QAction("Settings", self)
        action_about = QAction("About", self)
        # Action connections
        action_settings.triggered.connect(lambda: self.open_settings())
        action_about.triggered.connect(lambda: self.open_about())
        self.hamburger_menu.addActions([action_settings, action_about])
        # Attach menu to button
        self.menu_button.setMenu(self.hamburger_menu)
        self.menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.header_layout.addWidget(self.menu_button)

        # Tip to get more options
        self.bar_visibility_label = QLabel("Tip: Press 'alt' to show more config options.")
        font = self.bar_visibility_label.font()
        font.setPointSize(9)
        font.setItalic(True)
        self.bar_visibility_label.setFont(font)
        self.bar_visibility_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Home page image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        pixmap = icon.pixmap(64, 64)
        self.image_label.setPixmap(pixmap)

        # Program title
        self.label = QLabel("<h2>Super Duper Secret</h2>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.unlock_button = QPushButton("Unlock Safe")
        self.unlock_button.setFixedHeight(40)
        self.unlock_button.clicked.connect(self.clicked_unlock_button)

        self.new_safe_button = QPushButton("New Safe")
        self.new_safe_button.setFixedHeight(40)
        self.new_safe_button.clicked.connect(self.clicked_new_safe_button)

        self.verify_file_button = QPushButton("Verify File")
        self.verify_file_button.clicked.connect(self.clicked_verify_file_button)

        # Add to layout
        #layout.addWidget(self.bar_visibility_label)
        layout.addLayout(self.header_layout)
        #layout.addStretch() # Push header to top
        layout.addWidget(self.image_label)
        layout.addWidget(self.label)
        layout.addWidget(self.unlock_button)
        layout.addWidget(self.new_safe_button)
        layout.addWidget(self.verify_file_button)

    def clicked_unlock_button(self):        
        self.on_unlock()

    def clicked_new_safe_button(self):        
        self.on_new()

    def clicked_verify_file_button(self):
        self.on_verify()

    def open_settings(self):
        dialog = SettingsWindow(self)
        dialog.exec()

    def open_about(self):
        dialog = AboutWindow(self)
        dialog.exec()

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__()

        # Get current application instance (used to set themes)
        self.app = QApplication.instance()

        self.setWindowTitle("Settings")
        self.setFixedWidth(300)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Theme select row
        self.theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Theme select:")
        self.theme_box = QComboBox()
        self.theme_box.addItems(QStyleFactory.keys())
        self.theme_box.currentTextChanged.connect(self.set_theme)

        self.theme_layout.addWidget(self.theme_label)
        self.theme_layout.addWidget(self.theme_box)

        # Set dark theme
        self.dark_override_checkbox = QCheckBox("Force Dark Theme")

        # Add to main layout
        self.layout.addLayout(self.theme_layout)
        self.layout.addWidget(self.dark_override_checkbox, alignment=Qt.AlignmentFlag.AlignHCenter)

    def set_theme(self, theme):
        self.app.setStyle(theme)

class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()
        self.setWindowTitle("About")
        self.setFixedWidth(300)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        full_name_label = QLabel("Super Duper Secret (SDS)")
        version_label = QLabel(f"Version: {__init__.__version__}")
        repo_label = QLabel("Repository: https://github.com/ner216/sds")

        self.layout.addWidget(full_name_label)
        self.layout.addWidget(version_label)
        self.layout.addWidget(repo_label)