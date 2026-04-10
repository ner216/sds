import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import qdarktheme
import argparse

from utils.config import Config
from ui.cli import CLI

def main():
    # Initialize config object for managing program settings
    config = Config()
    default_safe_path = config.get_default_safe_path()

    parser = argparse.ArgumentParser(description="A simple password manager.")
    parser.add_argument("-d", "--delete-config", action="store_true", help="Delete all config data created by SDS")
    parser.add_argument("-g", "--get-password", type=str, help="Get a password from the default safe.")
    parser.add_argument("-l", "--list", action="store_true", help="List saved password entries.")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Start GUI if no args are given
        start_gui()
    elif args.list == True:
        CLI(default_safe_path).list_entries()
    elif args.delete_config == True:
        config.delete_all()
    elif args.get_password:
        CLI(default_safe_path).get_password(args.get_password)

def start_gui():
    app = QApplication(sys.argv)
    stylesheet = qdarktheme.load_stylesheet("dark")
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()