"""Style QSS dla aplikacji Zarządca Bloku — Light Mode, Green Gradient."""

MAIN_STYLE = """

/* ============================================
   GLOBALNE
   ============================================ */

QMainWindow {
    background-color: #f4f6f8;
}

* {
    font-family: "Segoe UI", "Arial", sans-serif;
    color: #212121;
}

/* ============================================
   PANEL NAWIGACJI BOCZNEJ (jasny, miękki)
   ============================================ */

#nav_panel {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #e8f5e9,
        stop:1 #f1f8e9
    );
    min-width: 230px;
    max-width: 230px;
    border-right: 1px solid #c8e6c9;
}

#nav_panel QPushButton {
    background-color: transparent;
    color: #37474f;
    border: none;
    padding: 13px 22px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    border-radius: 12px;
    margin: 2px 10px;
}

#nav_panel QPushButton:hover {
    background-color: rgba(76, 175, 80, 0.12);
    color: #2e7d32;
}

#nav_panel QPushButton:checked,
#nav_panel QPushButton[active="true"] {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #43a047,
        stop:1 #66bb6a
    );
    color: white;
    font-weight: 600;
}

#app_title {
    color: #1b5e20;
    font-size: 17px;
    font-weight: 800;
    padding: 24px 22px 6px 22px;
    letter-spacing: 0.3px;
}

#app_subtitle {
    color: #558b2f;
    font-size: 11px;
    padding: 0px 22px 22px 22px;
    font-weight: 500;
}

/* ============================================
   KARTY STATYSTYCZNE
   ============================================ */

.stat-card {
    background-color: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #e0e0e0;
}

.stat-card:hover {
    border-color: #66bb6a;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #212121;
}

.stat-label {
    font-size: 12px;
    color: #757575;
    font-weight: 500;
}

/* ============================================
   TABELE
   ============================================ */

QTableWidget {
    background-color: white;
    color: #212121;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    gridline-color: #f5f5f5;
    selection-background-color: #e8f5e9;
    selection-color: #212121;
    font-size: 12px;
    outline: none;
}

QTableWidget::item {
    padding: 7px 10px;
    border-bottom: 1px solid #fafafa;
}

QTableWidget::item:selected {
    background-color: #e8f5e9;
}

QHeaderView::section {
    background-color: #fafafa;
    color: #424242;
    border: none;
    border-bottom: 2px solid #e0e0e0;
    padding: 9px 10px;
    font-weight: 600;
    font-size: 12px;
}

/* ============================================
   PRZYCISKI — główny akcent zielony gradient
   ============================================ */

QPushButton {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #43a047,
        stop:1 #66bb6a
    );
    color: white;
    border: none;
    padding: 9px 18px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    min-height: 34px;
}

QPushButton:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #388e3c,
        stop:1 #43a047
    );
}

QPushButton:pressed {
    background-color: #2e7d32;
}

QPushButton:disabled {
    background-color: #bdbdbd;
    color: #9e9e9e;
}

QPushButton[class="secondary"] {
    background-color: #eceff1;
    color: #546e7a;
    border: 1px solid #cfd8dc;
}

QPushButton[class="secondary"]:hover {
    background-color: #cfd8dc;
    color: #37474f;
}

QPushButton[class="danger"] {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #e53935,
        stop:1 #ef5350
    );
}

QPushButton[class="danger"]:hover {
    background-color: #c62828;
}

QPushButton[class="success"] {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2e7d32,
        stop:1 #43a047
    );
}

QPushButton[class="success"]:hover {
    background-color: #1b5e20;
}

QPushButton[class="warning"] {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #f9a825,
        stop:1 #fbc02d
    );
    color: #212121;
}

QPushButton[class="warning"]:hover {
    background-color: #f57f17;
}

/* ============================================
   POLA FORMULARZY
   ============================================ */

QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox, QTextEdit {
    border: 1.5px solid #e0e0e0;
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 12px;
    background-color: white;
    min-height: 30px;
    color: #212121;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus, QTextEdit:focus {
    border-color: #66bb6a;
    border-width: 2px;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: white;
    color: #212121;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    selection-background-color: #e8f5e9;
    selection-color: #212121;
    outline: none;
}

/* ============================================
   ETYKIETY
   ============================================ */

QLabel {
    color: #424242;
    font-size: 12px;
}

/* ============================================
   GROUP BOX
   ============================================ */

QGroupBox {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    margin-top: 16px;
    padding-top: 20px;
    background-color: white;
    font-weight: 600;
    font-size: 13px;
    color: #212121;
}

QGroupBox::title {
    subcontrol-origin: margin;
    padding: 2px 14px;
    color: #2e7d32;
}

/* ============================================
   SCROLLBAR (subtelny, zaokrąglony)
   ============================================ */

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    border-radius: 4px;
    margin: 4px 2px;
}

QScrollBar::handle:vertical {
    background: #c8e6c9;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #a5d6a7;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    border-radius: 4px;
    margin: 2px 4px;
}

QScrollBar::handle:horizontal {
    background: #c8e6c9;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #a5d6a7;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ============================================
   PANEL FILTRÓW
   ============================================ */

#filter_panel {
    background-color: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 12px;
}

/* ============================================
   NAGŁÓWEK WIDOKU
   ============================================ */

.view-title {
    font-size: 22px;
    font-weight: 700;
    color: #212121;
}

/* ============================================
   DIALOGI
   ============================================ */

QDialog {
    background-color: #fafafa;
    border-radius: 16px;
    color: #212121;
}
"""
