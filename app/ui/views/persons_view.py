"""Widok osób — tabela z CRUD i filtrami."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QLineEdit,
    QMessageBox, QHeaderView, QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.person_service import PersonService
from app.ui.dialogs.person_dialog import PersonDialog
from app.enums import PersonRole
from app.utils.formatting import format_date, bool_to_text


class PersonsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Osoby")
        header.setProperty("class", "view-title")
        layout.addWidget(header)

        # Panel filtrów
        filter_panel = QWidget()
        filter_panel.setObjectName("filter_panel")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        self.filter_name = QLineEdit()
        self.filter_name.setPlaceholderText("Imię lub Nazwisko...")
        self.filter_name.setMaximumWidth(150)
        filter_layout.addWidget(self.filter_name)

        self.filter_role = QComboBox()
        self.filter_role.addItem("Wszystkie role", "")
        for r in PersonRole:
            self.filter_role.addItem(r.label, r.value)
        filter_layout.addWidget(self.filter_role)

        self.filter_active = QComboBox()
        self.filter_active.addItem("Wszyscy", None)
        self.filter_active.addItem("Tylko aktywni", True)
        self.filter_active.addItem("Nieaktywni", False)
        filter_layout.addWidget(self.filter_active)

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
        btn_add.clicked.connect(self.add_person)
        action_layout.addWidget(btn_add)

        btn_edit = QPushButton(" Edytuj")
        btn_edit.setIcon(get_icon("pencil"))
        btn_edit.setIconSize(QSize(18, 18))
        btn_edit.clicked.connect(self.edit_person)
        action_layout.addWidget(btn_edit)

        btn_delete = QPushButton(" Usuń")
        btn_delete.setIcon(get_icon("trash"))
        btn_delete.setIconSize(QSize(18, 18))
        btn_delete.setProperty("class", "danger")
        btn_delete.clicked.connect(self.delete_person)
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
            "ID", "Nazwisko i Imię", "Telefon", "E-mail", "Rola", "Aktywny", "Wprowadzenie", "Powiązane Mieszkania"
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
        self.filter_name.clear()
        self.filter_role.setCurrentIndex(0)
        self.filter_active.setCurrentIndex(0)
        self.refresh()

    def refresh(self):
        try:
            session = get_session()
            persons = PersonService.filter_persons(
                session,
                name=self.filter_name.text(),
                role=self.filter_role.currentData(),
                is_active=self.filter_active.currentData(),
            )

            self.table.setRowCount(0)
            for p in persons:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
                self.table.setItem(row, 1, QTableWidgetItem(f"{p.last_name} {p.first_name}"))
                self.table.setItem(row, 2, QTableWidgetItem(p.phone or "—"))
                self.table.setItem(row, 3, QTableWidgetItem(p.email or "—"))
                self.table.setItem(row, 4, QTableWidgetItem(p.role))

                active_item = QTableWidgetItem(bool_to_text(p.is_active))
                if p.is_active:
                    active_item.setForeground(Qt.GlobalColor.darkGreen)
                else:
                    active_item.setForeground(Qt.GlobalColor.darkGray)

                self.table.setItem(row, 5, active_item)
                self.table.setItem(row, 6, QTableWidgetItem(format_date(p.move_in_date)))

                # Zbierz numery mieszkań, do których jest przypisana ta osoba
                apt_numbers = []
                for link in p.apartment_links:
                    if link.apartment:
                        star = "*" if link.is_primary else ""
                        apt_numbers.append(f"{link.apartment.number}{star}")

                apt_text = ", ".join(apt_numbers) if apt_numbers else "—"
                self.table.setItem(row, 7, QTableWidgetItem(apt_text))

            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować osób:\n{e}")

    def _get_selected_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(self.table.item(selected[0].row(), 0).text())

    def add_person(self):
        try:
            session = get_session()
            dialog = PersonDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                PersonService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać osoby:\n{e}")

    def edit_person(self):
        p_id = self._get_selected_id()
        if not p_id:
            QMessageBox.information(self, "Informacja", "Zaznacz osobę do edycji.")
            return

        try:
            session = get_session()
            p = PersonService.get_by_id(session, p_id)
            if p:
                dialog = PersonDialog(self, p)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    PersonService.update(session, p_id, **data)
                    self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się edytować osoby:\n{e}")

    def delete_person(self):
        p_id = self._get_selected_id()
        if not p_id:
            QMessageBox.information(self, "Informacja", "Zaznacz osobę do usunięcia.")
            return

        reply = QMessageBox.question(
            self, "Potwierdzenie",
            "Czy na pewno chcesz usunąć tę osobę?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_session()
                PersonService.delete(session, p_id)
                session.close()
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć osoby:\n{e}")
