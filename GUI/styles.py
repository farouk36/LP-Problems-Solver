def get_dark_stylesheet():
    return """
        QMainWindow, QWidget, QTabWidget, QTableWidget, QTextEdit, QScrollArea {
            background-color: #1A202C;
            color: #E2E8F0;
        }

        QTabWidget::pane {
            border: 1px solid #4A5568;
        }

        QTabBar::tab {
            background-color: #2D3748;
            color: #A0AEC0;
            padding: 8px 16px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }

        QTabBar::tab:selected {
            background-color: #3182CE;
            color: #FFFFFF;
        }

        QHeaderView::section {
            background-color: #2D3748;
            color: #E2E8F0;
            padding: 6px;
            border: 1px solid #4A5568;
            font-weight: bold;
        }

        QTableWidget {
            gridline-color: #4A5568;
            selection-background-color: #4299E1;
            selection-color: #FFFFFF;
            alternate-background-color: #2D3748;
        }

        QTableWidget::item {
            border-bottom: 1px solid #4A5568;
            padding: 4px;
        }

        QTableWidget::item:alternate {
            background-color: #2D3748;
        }

        QGroupBox {
            border: 1px solid #4A5568;
            border-radius: 6px;
            margin-top: 20px;
            font-weight: bold;
            color: #63B3ED;
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2D3748, stop:1 #1A202C);
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            background-color: #1A202C;
        }

        QPushButton {
            background-color: #3182CE;
            color: #FFFFFF;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #4299E1;
        }

        QPushButton:pressed {
            background-color: #2B6CB0;
        }

        QPushButton#solve_button {
            background-color: #38A169;
            font-size: 14px;
        }

        QPushButton#solve_button:hover {
            background-color: #48BB78;
        }

        QPushButton#solve_button:pressed {
            background-color: #2F855A;
        }

        QComboBox, QSpinBox, QLineEdit {
            background-color: #2D3748;
            color: #E2E8F0;
            border: 1px solid #4A5568;
            border-radius: 4px;
            padding: 6px
            selection-background-color: #4299E1;
        }
        
        QComboBox, QLineEdit{
        padding=20px
        }
        QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
            border: 1px solid #63B3ED;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left: 1px solid #4A5568;
        }

        QRadioButton {
            color: #E2E8F0;
            spacing: 8px;
            padding: 2px;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #4A5568;
        }

        QRadioButton::indicator:checked {
            background-color: #3182CE;
            border: 2px solid #4A5568;
        }

        QRadioButton:hover {
            color: #63B3ED;
        }

        QTextEdit {
            background-color: #2D3748;
            color: #E2E8F0;
            border: 1px solid #4A5568;
            border-radius: 4px;
            selection-background-color: #4299E1;
            selection-color: #FFFFFF;
        }

        QStatusBar {
            background-color: #2D3748;
            color: #A0AEC0;
            border-top: 1px solid #4A5568;
        }

        QScrollBar:vertical {
            border: none;
            background-color: #2D3748;
            width: 12px;
            margin: 12px 0 12px 0;
        }

        QScrollBar::handle:vertical {
            background-color: #4A5568;
            min-height: 20px;
            border-radius: 3px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #63B3ED;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 12px;
            background: none;
        }

        QScrollBar:horizontal {
            border: none;
            background-color: #2D3748;
            height: 12px;
            margin: 0 12px 0 12px;
        }

        QScrollBar::handle:horizontal {
            background-color: #4A5568;
            min-width: 20px;
            border-radius: 3px;
        }

        QScrollBar::handle:horizontal:hover {
            background-color: #63B3ED;
        }
    """