"""Dialog dodawania / edycji osoby."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QCheckBox, QTextEdit, QPushButton, QMessageBox,
    QLabel, QDateEdit
)
from PySide6.QtCore import Qt, QDate

from app.enums import PersonRole
from app.utils.validators import validate_not_empty, validate_email, validate_phone


class PersonDialog(QDialog):
    def __init__(self, parent=None, person=None):
        super().__init__(parent)
        self.person = person
        self.setWindowTitle("Edytuj osobę" if person else "Dodaj osobę")
        self.setMinimumWidth(450)
        self._init_ui()
        if person:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(self.windowTitle())
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #2e7d32;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Imię")
        form.addRow("Imię *:", self.first_name_edit)

        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Nazwisko")
        form.addRow("Nazwisko *:", self.last_name_edit)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("np. 600123456")
        form.addRow("Telefon:", self.phone_edit)

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("np. jan@email.pl")
        form.addRow("E-mail:", self.email_edit)

        self.pesel_edit = QLineEdit()
        self.pesel_edit.setPlaceholderText("11 cyfr (opcjonalnie)")
        self.pesel_edit.setMaxLength(11)
        form.addRow("PESEL:", self.pesel_edit)

        self.role_combo = QComboBox()
        for r in PersonRole:
            self.role_combo.addItem(r.label, r.value)
        form.addRow("Rola *:", self.role_combo)

        self.move_in_date = QDateEdit()
        self.move_in_date.setCalendarPopup(True)
        self.move_in_date.setDate(QDate.currentDate())
        form.addRow("Data wprowadzenia:", self.move_in_date)

        self.is_active_check = QCheckBox("Aktywny")
        self.is_active_check.setChecked(True)
        form.addRow("", self.is_active_check)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        form.addRow("Notatki:", self.notes_edit)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Anuluj")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Zapisz")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _load_data(self):
        p = self.person
        self.first_name_edit.setText(p.first_name)
        self.last_name_edit.setText(p.last_name)
        self.phone_edit.setText(p.phone or "")
        self.email_edit.setText(p.email or "")
        self.pesel_edit.setText(p.pesel or "")

        idx = self.role_combo.findData(p.role)
        if idx >= 0:
            self.role_combo.setCurrentIndex(idx)

        if p.move_in_date:
            self.move_in_date.setDate(QDate(p.move_in_date.year, p.move_in_date.month, p.move_in_date.day))

        self.is_active_check.setChecked(p.is_active)
        self.notes_edit.setPlainText(p.notes or "")

    def _save(self):
        errors = []
        err = validate_not_empty(self.first_name_edit.text(), "Imię")
        if err:
            errors.append(err)
        err = validate_not_empty(self.last_name_edit.text(), "Nazwisko")
        if err:
            errors.append(err)
        err = validate_email(self.email_edit.text())
        if err:
            errors.append(err)
        err = validate_phone(self.phone_edit.text())
        if err:
            errors.append(err)

        if errors:
            QMessageBox.warning(self, "Błąd walidacji", "\n".join(errors))
            return

        self.accept()

    def get_data(self) -> dict:
        qdate = self.move_in_date.date()
        from datetime import date
        move_in = date(qdate.year(), qdate.month(), qdate.day())
        return {
            "first_name": self.first_name_edit.text().strip(),
            "last_name": self.last_name_edit.text().strip(),
            "phone": self.phone_edit.text().strip() or None,
            "email": self.email_edit.text().strip() or None,
            "pesel": self.pesel_edit.text().strip() or None,
            "role": self.role_combo.currentData(),
            "move_in_date": move_in,
            "is_active": self.is_active_check.isChecked(),
            "notes": self.notes_edit.toPlainText().strip() or None,
        }
