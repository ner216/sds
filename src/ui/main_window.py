from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtGui import QAction
from qt_material import QtStyleTools, apply_stylesheet
from PyQt6.QtCore import Qt

from ui.verify_file_widget import VerifyFileWidget
from ui.startup_widget import StartupWidget
from ui.login_widget import LoginWidget
from ui.new_safe_widget import NewSafeWidget
from ui.password_list_widget import PasswordListWidget

from core.database import PasswordDB
from core.hash_logic import Hash
from ui.style import FUSION_DARK_STYLE, ADWAITA_DARK_STYLE  # Style sheets are stored in this file
from utils.config import AppConfig
import time

class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = AppConfig()
        
        self.set_initial_theme()
        
        # Menu Bar
        self.menu_bar = self.menuBar()
        self.menu_bar.setVisible(False)

        # Theme menu for bar
        theme_menu = self.menu_bar.addMenu("Themes")

        default_theme = QAction("Default", self)
        default_theme.triggered.connect(lambda checked: self.change_color('None'))
        theme_menu.addAction(default_theme)

        light_mode = theme_menu.addMenu("Light Mode")

        LIGHT_STYLE_LIST = [ ("Red", 'light_red.xml'),
                    ("Orange", 'light_amber.xml'),
                    ("Yellow", 'light_yellow.xml'),
                    ("Green", 'light_lightgreen.xml'),
                    ("Teal", 'light_teal.xml'),
                    ("Blue", 'light_blue.xml'),
                    ("Light Blue", 'light_cyan.xml'),
                    ("Cyan", 'light_cyan_500.xml'),
                    ("Purple", 'light_purple.xml'),
                    ("Pink", 'light_pink.xml')
                    ]
        
        for color_name, theme in LIGHT_STYLE_LIST:
            action = QAction(color_name, self)
            action.triggered.connect(lambda checked, t=theme: self.change_color(t))
            light_mode.addAction(action)
    

        dark_mode = theme_menu.addMenu("Dark Mode")

        DARK_STYLE_LIST = [ ("Red", 'dark_red.xml'),
                    ("Orange", 'dark_amber.xml'),
                    ("Yellow", 'dark_yellow.xml'),
                    ("Green", 'dark_lightgreen.xml'),
                    ("Teal", 'dark_teal.xml'),
                    ("Blue", 'dark_blue.xml'),
                    ("Cyan", 'dark_cyan.xml'),
                    ("Purple", 'dark_purple.xml'),
                    ("Pink", 'dark_pink.xml'),
                    ("Fusion Dark", FUSION_DARK_STYLE),
                    ("Adwaita Dark", ADWAITA_DARK_STYLE)
                    ]
        
        for color_name, theme in DARK_STYLE_LIST:
            action = QAction(color_name, self)
            action.triggered.connect(lambda checked, t=theme: self.change_color(t))
            dark_mode.addAction(action)

        style_mode = theme_menu.addMenu("Stylesheets")

        STYLE_LIST = [ ("Fusion Dark", FUSION_DARK_STYLE),
                        ("Adwaita Dark", ADWAITA_DARK_STYLE)
                    ]
        
        for style_name, theme in STYLE_LIST:
            action = QAction(style_name, self)
            action.triggered.connect(lambda checked, t=theme: self.change_style(t))
            style_mode.addAction(action)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setFixedSize(500, 370)

        # Initial page to show on startup
        self.startup_screen = StartupWidget(on_unlock=self.go_to_login, on_new=self.go_to_new_safe, on_verify=self.go_to_verify_file)

        # Verify file page
        self.verify_file = VerifyFileWidget()
        self.verify_file.back_requested.connect(self.go_to_startup)
        self.verify_file.verify_file.connect(self.handle_verify_file)
        
        # New safe page
        self.new_safe = NewSafeWidget()
        self.new_safe.back_requested.connect(self.go_to_startup)
        self.new_safe.create_safe.connect(self.handle_create_safe)

        # Login page
        self.login = LoginWidget()
        self.login.back_requested.connect(self.go_to_startup)
        self.login.decrypt_safe.connect(self.handle_enter_safe)

        self.stack.addWidget(self.verify_file)
        self.stack.addWidget(self.startup_screen)
        self.stack.addWidget(self.new_safe)
        self.stack.addWidget(self.login)

        # Start the initial GUI window (startup)
        self.go_to_startup()

    def handle_enter_safe(self, db_file_path: str, passphrase: str):
        try:
            db = PasswordDB(db_file_path, passphrase)
            db.load_db()
            self.password_view = PasswordListWidget(db)
            self.password_view.back_requested.connect(self.go_to_startup)
            
            self.stack.addWidget(self.password_view)
            self.stack.setCurrentWidget(self.password_view)
            self.setWindowTitle("Super Duper Secret - Passwords")
        except Exception as e:
            print(f"Error: Login failed!\n {e}")
            self.login.failed_attempts += 1
            if self.login.failed_attempts >= 3:
                # Set lockout for 30 seconds
                self.login.lockout_end_time = time.time() + 15
                self.login.login_button.setEnabled(False)
                self.login.cooldown_timer.start(1000)
            
            QMessageBox.information(self, "Invalid Login", "Password is wrong or database file is not valid!")

    def handle_create_safe(self, db_file_path: str, passphrase: str):
        try:
            db = PasswordDB(db_file_path, passphrase)
            self.password_view = PasswordListWidget(db)
            self.password_view.back_requested.connect(self.go_to_startup)
            
            self.stack.addWidget(self.password_view)
            self.stack.setCurrentWidget(self.password_view)
            self.setWindowTitle("Super Duper Secret - Passwords")
        except Exception as e:
            print(f"Error: Unable to create new safe!\n {e}")
            QMessageBox.information(self, "Error", "Unable to create new safe!")

    def handle_verify_file(self, file_path: str, known_hash: str):
        trimmed_known_hash = known_hash.removeprefix("sha256:")
        calculated_hash = Hash.get_file_hash(file_path)
        verified = (calculated_hash == trimmed_known_hash)
        if verified == True:
            QMessageBox.information(self, "Success", f"File verified successfully!\nOriginal: {trimmed_known_hash}\nCalculated: {calculated_hash}")
        else:
            QMessageBox.information(self, "Error", f"File hashes do not match; the file may be compromised!\nOriginal: {trimmed_known_hash}\nCalculated: {calculated_hash}")

    def go_to_verify_file(self):
        self.stack.setCurrentWidget(self.verify_file)
        self.setWindowTitle("Super Duper Secret - Verify")

    def go_to_startup(self):
        self.stack.setCurrentWidget(self.startup_screen)
        self.setWindowTitle("Super Duper Secret")

    def go_to_new_safe(self):
        self.stack.setCurrentWidget(self.new_safe)
        self.setWindowTitle("Super Duper Secret - New")

    def go_to_login(self):
        self.stack.setCurrentWidget(self.login)
        self.setWindowTitle("Super Duper Secret - Login")

    def change_color(self, color):
        self.setStyleSheet("")
        apply_stylesheet(self,theme=color)
        self.config.add_or_update_entry(key="preferred_theme_type", value="color")
        self.config.add_or_update_entry(key="color", value=color)

    def change_style(self, style):
        lambda checked: self.change_color('None')
        self.setStyleSheet(style)
        self.config.add_or_update_entry(key="preferred_theme_type", value="style")
        self.config.add_or_update_entry(key="style", value=style)

    def set_initial_theme(self):
        preferred_theme_type = self.config.get_entry("preferred_theme_type")

        if preferred_theme_type == "style":
            self.change_style(self.config.get_entry("style"))
        elif preferred_theme_type == "color":
            self.change_color(self.config.get_entry("color"))
        else:
            self.setStyleSheet(ADWAITA_DARK_STYLE)

    def keyPressEvent(self, event):
        # Check if the Alt key was pressed alone
        if event.key() == Qt.Key.Key_Alt:
            # Toggle visibility
            is_visible = self.menu_bar.isVisible()
            self.menu_bar.setVisible(not is_visible)
        
        # Always call the superclass event to keep default behavior intact
        super().keyPressEvent(event)
