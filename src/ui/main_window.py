from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox

from ui.verify_file_widget import VerifyFileWidget
from ui.startup_widget import StartupWidget
from ui.login_widget import LoginWidget
from ui.new_safe_widget import NewSafeWidget
from ui.password_list_widget import PasswordListWidget

from core.database import PasswordDB
from core.hash_logic import Hash
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setMinimumSize(450, 250)

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