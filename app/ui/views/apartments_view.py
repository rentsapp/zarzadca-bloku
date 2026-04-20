"""Widok mieszkań — tabela z CRUD i filtrami."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QLineEdit,
    QMessageBox, QHeaderView, QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.apartment_service import ApartmentService
from app.ui.dialogs.apartment_dialog import ApartmentDialog
from app.enums import ApartmentStatus
from app.utils.formatting import format_currency, format_area


class ApartmentsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Mieszkania")
        header.setProperty("class", "view-title")
        layout.addWidget(header)

        # Panel filtrów
        filter_panel = QWidget()
        filter_panel.setObjectName("filter_panel")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        self.filter_number = QLineEdit()
        self.filter_number.setPlaceholderText("Numer...")
        self.filter_number.setMaximumWidth(100)
        filter_layout.addWidget(self.filter_number)

        self.filter_staircase = QComboBox()
        self.filter_staircase.addItem("Wszystkie klatki", "")
        filter_layout.addWidget(self.filter_staircase)

        self.filter_status = QComboBox()
        self.filter_status.addItem("Wszystkie statusy", "")
        for s in ApartmentStatus:
            self.filter_status.addItem(s.label, s.value)
        filter_layout.addWidget(self.filter_status)

        btn_filter = QPushButton("Filtruj")
        btn_filter.setProperty("class", "secondary")
        btn_filter.clicked.connect(self.refresh)
        filter_layout.addWidget(btn_filter)

        btn_reset = QPushButton("Resetuj")
        btn_reset.setProperty("class", "secondary")
        btn_reset.clicked.connect(self._reset_filters)
        filter_layout.addWidget(btn_reset)

        filter_layout.addStretch()
        layout.addWidget(filter_panel)

        # Panel akcji
        action_layout = QHBoxLayout()
        btn_add = QPushButton(" Dodaj")
        btn_add.setIcon(get_icon("plus"))
        btn_add.setIconSize(QSize(18, 18))
        btn_add.clicked.connect(self.add_apartment)
        action_layout.addWidget(btn_add)

        btn_edit = QPushButton(" Edytuj")
        btn_edit.setIcon(get_icon("pencil"))
        btn_edit.setIconSize(QSize(18, 18))
        btn_edit.clicked.connect(self.edit_apartment)
        action_layout.addWidget(btn_edit)

        btn_delete = QPushButton(" Usuń")
        btn_delete.setIcon(get_icon("trash"))
        btn_delete.setIconSize(QSize(18, 18))
        btn_delete.setProperty("class", "danger")
        btn_delete.clicked.connect(self.delete_apartment)
        action_layout.addWidget(btn_delete)

        action_layout.addStretch()
        btn_refresh = QPushButton(" Odśwież")
        btn_refresh.setIcon(get_icon("refresh"))
        btn_refresh.setIconSize(QSize(18, 18))
        btn_refresh.setProperty("class", "secondary")
        btn_refresh.clicked.connect(self.refresh)
        action_layout.addWidget(btn_refresh)
        layout.addLayout(action_layout)

        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Numer", "Klatka", "Piętro", "Metraż", "Pokoje", "Status", "Czynsz bazowy"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.hideColumn(0)  # Ukryj ID
        layout.addWidget(self.table)

    def _reset_filters(self):
        self.filter_number.clear()
        self.filter_staircase.setCurrentIndex(0)
        self.filter_status.setCurrentIndex(0)
        self.refresh()

    def _update_staircases_combo(self):
        current = self.filter_staircase.currentData()
        self.filter_staircase.clear()
        self.filter_staircase.addItem("Wszystkie klatki", "")
        try:
            session = get_session()
            staircases = ApartmentService.get_staircases(session)
            for sc in staircases:
                self.filter_staircase.addItem(sc, sc)
            session.close()

            idx = self.filter_staircase.findData(current)
            if idx >= 0:
                self.filter_staircase.setCurrentIndex(idx)
        except Exception as e:
            print(f"Błąd ładowania klatek: {e}")

    def refresh(self):
        self._update_staircases_combo()
        try:
            session = get_session()
            apartments = ApartmentService.filter_apartments(
                session,
                number=self.filter_number.text(),
                staircase=self.filter_staircase.currentData(),
                status=self.filter_status.currentData(),
            )

            self.table.setRowCount(0)
            for apt in apartments:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(str(apt.id)))
                self.table.setItem(row, 1, QTableWidgetItem(apt.number))
                self.table.setItem(row, 2, QTableWidgetItem(apt.staircase))
                self.table.setItem(row, 3, QTableWidgetItem(str(apt.floor)))
                self.table.setItem(row, 4, QTableWidgetItem(format_area(apt.area)))
                self.table.setItem(row, 5, QTableWidgetItem(str(apt.rooms)))

                status_item = QTableWidgetItem(apt.status)
                if apt.status == "wolne":
                    status_item.setForeground(Qt.GlobalColor.darkGray)
                elif apt.status == "zamieszkane":
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif apt.status == "w remoncie":
                    status_item.setForeground(Qt.GlobalColor.red)
                elif apt.status == "zarezerwowane":
                    status_item.setForeground(Qt.GlobalColor.darkYellow)

                self.table.setItem(row, 6, status_item)
                self.table.setItem(row, 7, QTableWidgetItem(format_currency(apt.base_rent)))

            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować mieszkań:\n{e}")

    def _get_selected_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(self.table.item(selected[0].row(), 0).text())

    def add_apartment(self):
        try:
            session = get_session()
            dialog = ApartmentDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                ApartmentService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać mieszkania:\n{e}")

    def edit_apartment(self):
        apt_id = self._get_selected_id()
        if not apt_id:
            QMessageBox.information(self, "Informacja", "Zaznacz mieszkanie do edycji.")
            return

        try:
            session = get_session()
            apt = ApartmentService.get_by_id(session, apt_id)
            if apt:
                dialog = ApartmentDialog(self, apt)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    # building_id nie można zmienić z tego widoku (jest stały w MVP)
                    del data['building_id']
                    ApartmentService.update(session, apt_id, **data)
                    self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się edytować mieszkania:\n{e}")

    def delete_apartment(self):
        apt_id = self._get_selected_id()
        if not apt_id:
            QMessageBox.information(self, "Informacja", "Zaznacz mieszkanie do usunięcia.")
            return

        reply = QMessageBox.question(
            self, "Potwierdzenie",
            "Czy na pewno chcesz usunąć to mieszkanie?\nUsunięte zostaną również powiązane z nim płatności i usterki.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_session()
                ApartmentService.delete(session, apt_id)
                session.close()
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć mieszkania:\n{e}")
