import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget

app = QApplication(sys.argv)
w = QWidget()
with open("app/ui/styles.py", "r", encoding="utf-8") as f:
    text = f.read()
    styles = text.split('MAIN_STYLE = """')[1].split('"""')[0]

w.setStyleSheet(styles)
print("No errors" if not app.styleSheet() else "Style set")
