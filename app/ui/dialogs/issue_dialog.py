"""Dialog dodawania / edycji usterki."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QDoubleSpinBox, QTextEdit, QPushButton, QMessageBox,
    QLabel, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import date

from app.enums import IssuePriority, IssueStatus
from app.database import get_session
from app.models.apartment import Apartment
from app.utils.validators import validate_not_empty


class IssueDialog(QDialog):
    def __init__(self, parent=None, issue=None, apartment_id=None):
        super().__init__(parent)
        self.issue = issue
        self.preset_apartment_id = apartment_id
        self.setWindowTitle("Edytuj usterkę" if issue else "Dodaj usterkę")
        self.setMinimumWidth(500)
        self._init_ui()
        if issue:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title_lbl = QLabel(self.windowTitle())
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #2e7d32;")
        layout.addWidget(title_lbl)

        form = QFormLayout()
        form.setSpacing(8)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Krótki opis usterki")
        form.addRow("Tytuł *:", self.title_edit)

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Szczegółowy opis problemu...")
        form.addRow("Opis *:", self.description_edit)

        # Mieszkanie (opcjonalne — usterka może dotyczyć części wspólnej)
        self.apartment_combo = QComboBox()
        self.apartment_combo.addItem("— Część wspólna —", None)
        session = get_session()
        apartments = session.query(Apartment).order_by(Apartment.number).all()
        for apt in apartments:
            self.apartment_combo.addItem(f"Mieszkanie {apt.number} (kl. {apt.staircase})", apt.id)
        session.close()

        if self.preset_apartment_id:
            idx = self.apartment_combo.findData(self.preset_apartment_id)
            if idx >= 0:
                self.apartment_combo.setCurrentIndex(idx)
        form.addRow("Mieszkanie:", self.apartment_combo)

        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("np. Klatka B, 2. piętro (dla części wspólnych)")
        form.addRow("Lokalizacja:", self.location_edit)

        self.reporter_edit = QLineEdit()
        self.reporter_edit.setPlaceholderText("Imię i nazwisko zgłaszającego")
        form.addRow("Zgłaszający:", self.reporter_edit)

        self.reported_date = QDateEdit()
        self.reported_date.setCalendarPopup(True)
        self.reported_date.setDate(QDate.currentDate())
        form.addRow("Data zgłoszenia:", self.reported_date)

        self.priority_combo = QComboBox()
        for p in IssuePriority:
            self.priority_combo.addItem(p.label, p.value)
        self.priority_combo.setCurrentIndex(1)  # średni
        form.addRow("Priorytet:", self.priority_combo)

        self.status_combo = QComboBox()
        for s in IssueStatus:
            self.status_combo.addItem(s.label, s.value)
        form.addRow("Status:", self.status_combo)

        self.cost_spin = QDoubleSpinBox()
        self.cost_spin.setRange(0, 999999)
        self.cost_spin.setDecimals(2)
        self.cost_spin.setSuffix(" zł")
        form.addRow("Szacowany koszt:", self.cost_spin)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
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
        i = self.issue
        self.title_edit.setText(i.title)
        self.description_edit.setPlainText(i.description)

        if i.apartment_id:
            idx = self.apartment_combo.findData(i.apartment_id)
            if idx >= 0:
                self.apartment_combo.setCurrentIndex(idx)

        self.location_edit.setText(i.location_description or "")
        self.reporter_edit.setText(i.reporter_name or "")

        if i.reported_at:
            self.reported_date.setDate(QDate(i.reported_at.year, i.reported_at.month, i.reported_at.day))

        idx = self.priority_combo.findData(i.priority)
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)

        idx = self.status_combo.findData(i.status)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        self.cost_spin.setValue(i.estimated_cost or 0)
        self.notes_edit.setPlainText(i.notes or "")

    def _save(self):
        errors = []
        err = validate_not_empty(self.title_edit.text(), "Tytuł")
        if err:
            errors.append(err)
        err = validate_not_empty(self.description_edit.toPlainText(), "Opis")
        if err:
            errors.append(err)
        if errors:
            QMessageBox.warning(self, "Błąd walidacji", "\n".join(errors))
            return
        self.accept()

    def get_data(self) -> dict:
        qdate = self.reported_date.date()
        reported = date(qdate.year(), qdate.month(), qdate.day())
        apt_id = self.apartment_combo.currentData()
        return {
            "apartment_id": apt_id,
            "title": self.title_edit.text().strip(),
            "description": self.description_edit.toPlainText().strip(),
            "location_description": self.location_edit.text().strip() or None,
            "reporter_name": self.reporter_edit.text().strip() or None,
            "reported_at": reported,
            "priority": self.priority_combo.currentData(),
            "status": self.status_combo.currentData(),
            "estimated_cost": self.cost_spin.value() if self.cost_spin.value() > 0 else None,
            "notes": self.notes_edit.toPlainText().strip() or None,
        }
