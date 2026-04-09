import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import qdarktheme
import argparse

from utils.config_helper import HandleConfig

def main():
    parser = argparse.ArgumentParser(description="A simple password manager.")
    parser.add_argument("-d", "--delete-config", action="store_true", help="Delete all config data created by SDS")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Start GUI if no args are given
        start_gui()
    elif args.delete_config == True:
        HandleConfig.delete_config()


def start_gui():
    app = QApplication(sys.argv)
    stylesheet = qdarktheme.load_stylesheet("dark")
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()