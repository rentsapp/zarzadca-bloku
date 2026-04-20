"""Dialog dodawania / edycji płatności."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QPushButton, QMessageBox,
    QLabel, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import date

from app.enums import PaymentStatus
from app.database import get_session
from app.models.apartment import Apartment


class PaymentDialog(QDialog):
    def __init__(self, parent=None, payment=None, apartment_id=None):
        super().__init__(parent)
        self.payment = payment
        self.preset_apartment_id = apartment_id
        self.setWindowTitle("Edytuj płatność" if payment else "Dodaj płatność")
        self.setMinimumWidth(480)
        self._init_ui()
        if payment:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(self.windowTitle())
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #2e7d32;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        # Mieszkanie
        self.apartment_combo = QComboBox()
        session = get_session()
        apartments = session.query(Apartment).order_by(Apartment.number).all()
        for apt in apartments:
            self.apartment_combo.addItem(f"Mieszkanie {apt.number} (kl. {apt.staircase}, p. {apt.floor})", apt.id)
        session.close()
        if self.preset_apartment_id:
            idx = self.apartment_combo.findData(self.preset_apartment_id)
            if idx >= 0:
                self.apartment_combo.setCurrentIndex(idx)
        form.addRow("Mieszkanie *:", self.apartment_combo)

        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(date.today().month)
        form.addRow("Miesiąc *:", self.month_spin)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(2020, 2030)
        self.year_spin.setValue(date.today().year)
        form.addRow("Rok *:", self.year_spin)

        self.rent_spin = QDoubleSpinBox()
        self.rent_spin.setRange(0, 99999)
        self.rent_spin.setDecimals(2)
        self.rent_spin.setSuffix(" zł")
        self.rent_spin.setValue(1000.0)
        self.rent_spin.valueChanged.connect(self._recalculate)
        form.addRow("Czynsz:", self.rent_spin)

        self.utilities_spin = QDoubleSpinBox()
        self.utilities_spin.setRange(0, 99999)
        self.utilities_spin.setDecimals(2)
        self.utilities_spin.setSuffix(" zł")
        self.utilities_spin.setValue(300.0)
        self.utilities_spin.valueChanged.connect(self._recalculate)
        form.addRow("Media:", self.utilities_spin)

        self.other_spin = QDoubleSpinBox()
        self.other_spin.setRange(0, 99999)
        self.other_spin.setDecimals(2)
        self.other_spin.setSuffix(" zł")
        self.other_spin.setValue(50.0)
        self.other_spin.valueChanged.connect(self._recalculate)
        form.addRow("Inne opłaty:", self.other_spin)

        self.total_label = QLabel("0,00 zł")
        self.total_label.setStyleSheet("font-weight: 700; font-size: 14px; color: #212121;")
        form.addRow("Suma:", self.total_label)

        self.paid_spin = QDoubleSpinBox()
        self.paid_spin.setRange(0, 99999)
        self.paid_spin.setDecimals(2)
        self.paid_spin.setSuffix(" zł")
        self.paid_spin.setValue(0.0)
        self.paid_spin.valueChanged.connect(self._recalculate)
        form.addRow("Wpłacono:", self.paid_spin)

        self.balance_label = QLabel("0,00 zł")
        self.balance_label.setStyleSheet("font-weight: 700; color: #ef4444;")
        form.addRow("Saldo:", self.balance_label)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate(date.today().year, date.today().month, 10))
        form.addRow("Termin płatności:", self.due_date_edit)

        self.paid_date_edit = QDateEdit()
        self.paid_date_edit.setCalendarPopup(True)
        self.paid_date_edit.setDate(QDate.currentDate())
        self.paid_date_check = QPushButton("Brak daty zapłaty")
        self.paid_date_check.setCheckable(True)
        self.paid_date_check.setChecked(True)
        self.paid_date_check.setProperty("class", "secondary")
        self.paid_date_check.clicked.connect(self._toggle_paid_date)
        paid_date_layout = QHBoxLayout()
        paid_date_layout.addWidget(self.paid_date_edit)
        paid_date_layout.addWidget(self.paid_date_check)
        form.addRow("Data zapłaty:", paid_date_layout)
        self.paid_date_edit.setEnabled(False)

        self.status_combo = QComboBox()
        for s in PaymentStatus:
            self.status_combo.addItem(s.label, s.value)
        form.addRow("Status:", self.status_combo)

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
        self._recalculate()

    def _toggle_paid_date(self):
        checked = self.paid_date_check.isChecked()
        self.paid_date_edit.setEnabled(not checked)
        self.paid_date_check.setText("Brak daty zapłaty" if checked else "Ustaw datę zapłaty")

    def _recalculate(self):
        total = self.rent_spin.value() + self.utilities_spin.value() + self.other_spin.value()
        balance = total - self.paid_spin.value()
        self.total_label.setText(f"{total:,.2f} zł".replace(",", " ").replace(".", ","))
        color = "#22c55e" if balance <= 0 else "#ef4444"
        self.balance_label.setText(f"{balance:,.2f} zł".replace(",", " ").replace(".", ","))
        self.balance_label.setStyleSheet(f"font-weight: 700; color: {color};")

    def _load_data(self):
        p = self.payment
        idx = self.apartment_combo.findData(p.apartment_id)
        if idx >= 0:
            self.apartment_combo.setCurrentIndex(idx)
        self.month_spin.setValue(p.month)
        self.year_spin.setValue(p.year)
        self.rent_spin.setValue(p.rent_amount or 0)
        self.utilities_spin.setValue(p.utilities_amount or 0)
        self.other_spin.setValue(p.other_amount or 0)
        self.paid_spin.setValue(p.paid_amount or 0)
        if p.due_date:
            self.due_date_edit.setDate(QDate(p.due_date.year, p.due_date.month, p.due_date.day))
        if p.paid_date:
            self.paid_date_edit.setDate(QDate(p.paid_date.year, p.paid_date.month, p.paid_date.day))
            self.paid_date_check.setChecked(False)
            self.paid_date_edit.setEnabled(True)
            self.paid_date_check.setText("Ustaw datę zapłaty")
        idx = self.status_combo.findData(p.status)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)
        self.notes_edit.setPlainText(p.notes or "")
        self._recalculate()

    def _save(self):
        if self.apartment_combo.count() == 0:
            QMessageBox.warning(self, "Błąd", "Nie ma żadnych mieszkań w bazie.")
            return
        self.accept()

    def get_data(self) -> dict:
        qdue = self.due_date_edit.date()
        due = date(qdue.year(), qdue.month(), qdue.day())

        paid_date_val = None
        if not self.paid_date_check.isChecked():
            qpaid = self.paid_date_edit.date()
            paid_date_val = date(qpaid.year(), qpaid.month(), qpaid.day())

        total = self.rent_spin.value() + self.utilities_spin.value() + self.other_spin.value()
        balance = total - self.paid_spin.value()

        return {
            "apartment_id": self.apartment_combo.currentData(),
            "month": self.month_spin.value(),
            "year": self.year_spin.value(),
            "rent_amount": self.rent_spin.value(),
            "utilities_amount": self.utilities_spin.value(),
            "other_amount": self.other_spin.value(),
            "total_amount": total,
            "paid_amount": self.paid_spin.value(),
            "balance": balance,
            "due_date": due,
            "paid_date": paid_date_val,
            "status": self.status_combo.currentData(),
            "notes": self.notes_edit.toPlainText().strip() or None,
        }
