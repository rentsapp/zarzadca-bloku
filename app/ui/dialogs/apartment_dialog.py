"""Dialog dodawania / edycji mieszkania."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, QTextEdit,
    QPushButton, QMessageBox, QLabel
)
from PySide6.QtCore import Qt

from app.enums import ApartmentStatus, OwnershipType
from app.utils.validators import validate_not_empty, validate_positive_number, validate_positive_integer


class ApartmentDialog(QDialog):
    def __init__(self, parent=None, apartment=None, building_id: int = 1):
        super().__init__(parent)
        self.apartment = apartment
        self.building_id = building_id
        self.setWindowTitle("Edytuj mieszkanie" if apartment else "Dodaj mieszkanie")
        self.setMinimumWidth(450)
        self._init_ui()
        if apartment:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(self.windowTitle())
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #2e7d32;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        self.number_edit = QLineEdit()
        self.number_edit.setPlaceholderText("np. 1, 2A, 10")
        form.addRow("Numer mieszkania *:", self.number_edit)

        self.staircase_edit = QLineEdit()
        self.staircase_edit.setPlaceholderText("np. A, B, I")
        form.addRow("Klatka *:", self.staircase_edit)

        self.floor_spin = QSpinBox()
        self.floor_spin.setRange(0, 50)
        form.addRow("Piętro *:", self.floor_spin)

        self.area_spin = QDoubleSpinBox()
        self.area_spin.setRange(1.0, 500.0)
        self.area_spin.setDecimals(1)
        self.area_spin.setSuffix(" m²")
        self.area_spin.setValue(40.0)
        form.addRow("Metraż *:", self.area_spin)

        self.rooms_spin = QSpinBox()
        self.rooms_spin.setRange(1, 10)
        self.rooms_spin.setValue(2)
        form.addRow("Liczba pokoi *:", self.rooms_spin)

        self.status_combo = QComboBox()
        for s in ApartmentStatus:
            self.status_combo.addItem(s.label, s.value)
        form.addRow("Status:", self.status_combo)

        self.ownership_combo = QComboBox()
        for o in OwnershipType:
            self.ownership_combo.addItem(o.label, o.value)
        form.addRow("Typ własności:", self.ownership_combo)

        self.rent_spin = QDoubleSpinBox()
        self.rent_spin.setRange(0.0, 99999.0)
        self.rent_spin.setDecimals(2)
        self.rent_spin.setSuffix(" zł")
        self.rent_spin.setValue(1000.0)
        form.addRow("Czynsz bazowy:", self.rent_spin)

        self.balcony_check = QCheckBox("Posiada balkon")
        form.addRow("", self.balcony_check)

        self.storage_check = QCheckBox("Posiada komórkę lokatorską")
        form.addRow("", self.storage_check)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Dodatkowe uwagi...")
        form.addRow("Notatki:", self.notes_edit)

        layout.addLayout(form)

        # Przyciski
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
        a = self.apartment
        self.number_edit.setText(a.number)
        self.staircase_edit.setText(a.staircase)
        self.floor_spin.setValue(a.floor)
        self.area_spin.setValue(a.area)
        self.rooms_spin.setValue(a.rooms)

        idx = self.status_combo.findData(a.status)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        idx = self.ownership_combo.findData(a.ownership_type)
        if idx >= 0:
            self.ownership_combo.setCurrentIndex(idx)

        self.rent_spin.setValue(a.base_rent or 0)
        self.balcony_check.setChecked(a.has_balcony)
        self.storage_check.setChecked(a.has_storage)
        self.notes_edit.setPlainText(a.notes or "")

    def _save(self):
        errors = []
        err = validate_not_empty(self.number_edit.text(), "Numer mieszkania")
        if err:
            errors.append(err)
        err = validate_not_empty(self.staircase_edit.text(), "Klatka")
        if err:
            errors.append(err)

        if errors:
            QMessageBox.warning(self, "Błąd walidacji", "\n".join(errors))
            return

        self.accept()

    def get_data(self) -> dict:
        return {
            "building_id": self.building_id,
            "number": self.number_edit.text().strip(),
            "staircase": self.staircase_edit.text().strip(),
            "floor": self.floor_spin.value(),
            "area": self.area_spin.value(),
            "rooms": self.rooms_spin.value(),
            "status": self.status_combo.currentData(),
            "ownership_type": self.ownership_combo.currentData(),
            "base_rent": self.rent_spin.value(),
            "has_balcony": self.balcony_check.isChecked(),
            "has_storage": self.storage_check.isChecked(),
            "notes": self.notes_edit.toPlainText().strip() or None,
        }
