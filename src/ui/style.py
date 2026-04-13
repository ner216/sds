import qdarktheme

FUSION_DARK_STYLE = qdarktheme.load_stylesheet("dark")

ADWAITA_DARK_STYLE = """
    QWidget {
        border: 1px solid #393939;
        border-radius: 10px; 
        background-color: #393939; 
        color: #f9fafa;
    }

    QWidget:disabled {
        border: 1px solid #2d2d2d;
        background-color: #2d2d2d;
        color: #999999;
    }
    QWidget:focus {
        border: 2px solid #587392;
    }

    QWidget#Frame {
        background-color: #242424;
        border: none;
    }

    QLabel {
        border: none;
    }

    QPushButton {
        background-color: #303030;
        color: #ffffff;
        border: 1px solid #121212;
        border-bottom: 2px solid #121212;
        border-radius: 6px;
        padding: 6px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #454545;
    }

    QPushButton:pressed {
        background-color: #707070;
    }

    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #101010;
        border-radius: 6px;
        padding: 8px;
        selection-background-color: #3584e4;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #3584e4;
        padding: 7px;
    }
    """