"""Widok usterek — tabela z CRUD i filtrami."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QLineEdit,
    QMessageBox, QHeaderView, QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.issue_service import IssueService
from app.services.apartment_service import ApartmentService
from app.ui.dialogs.issue_dialog import IssueDialog
from app.enums import IssuePriority, IssueStatus
from app.utils.formatting import format_date


class IssuesView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Usterki i Zgłoszenia")
        header.setProperty("class", "view-title")
        layout.addWidget(header)

        # Panel filtrów
        filter_panel = QWidget()
        filter_panel.setObjectName("filter_panel")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        self.filter_title = QLineEdit()
        self.filter_title.setPlaceholderText("Szukaj w tytule...")
        self.filter_title.setMaximumWidth(150)
        filter_layout.addWidget(self.filter_title)

        self.filter_status = QComboBox()
        self.filter_status.addItem("Wszystkie statusy", "")
        for s in IssueStatus:
            self.filter_status.addItem(s.label, s.value)
        filter_layout.addWidget(self.filter_status)

        self.filter_priority = QComboBox()
        self.filter_priority.addItem("Wszystkie priorytety", "")
        for p in IssuePriority:
            self.filter_priority.addItem(p.label, p.value)
        filter_layout.addWidget(self.filter_priority)

        self.filter_apartment = QComboBox()
        self.filter_apartment.addItem("Wszystkie lokalizacje", None)
        filter_layout.addWidget(self.filter_apartment)

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
        btn_add = QPushButton(" Dodaj zgłoszenie")
        btn_add.setIcon(get_icon("plus"))
        btn_add.setIconSize(QSize(18, 18))
        btn_add.clicked.connect(self.add_issue)
        action_layout.addWidget(btn_add)

        btn_edit = QPushButton(" Edytuj")
        btn_edit.setIcon(get_icon("pencil"))
        btn_edit.setIconSize(QSize(18, 18))
        btn_edit.clicked.connect(self.edit_issue)
        action_layout.addWidget(btn_edit)

        btn_delete = QPushButton(" Usuń")
        btn_delete.setIcon(get_icon("trash"))
        btn_delete.setIconSize(QSize(18, 18))
        btn_delete.setProperty("class", "danger")
        btn_delete.clicked.connect(self.delete_issue)
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
            "ID", "Tytuł", "Lokalizacja", "Priorytet", "Status", "Zgłaszający", "Data", "Szac. koszt"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.hideColumn(0)  # Ukryj ID
        layout.addWidget(self.table)

    def _update_apartments_combo(self):
        current = self.filter_apartment.currentData()
        self.filter_apartment.clear()
        self.filter_apartment.addItem("Wszystkie lokalizacje", None)
        try:
            session = get_session()
            apartments = ApartmentService.get_all(session)
            for apt in apartments:
                self.filter_apartment.addItem(f"M. {apt.number}", apt.id)
            session.close()

            idx = self.filter_apartment.findData(current)
            if idx >= 0:
                self.filter_apartment.setCurrentIndex(idx)
        except Exception as e:
            print(f"Błąd ładowania mieszkań dla filtra usterek: {e}")

    def _reset_filters(self):
        self.filter_title.clear()
        self.filter_status.setCurrentIndex(0)
        self.filter_priority.setCurrentIndex(0)
        self.filter_apartment.setCurrentIndex(0)
        self.refresh()

    def refresh(self):
        self._update_apartments_combo()
        try:
            session = get_session()
            issues = IssueService.filter_issues(
                session,
                title=self.filter_title.text(),
                status=self.filter_status.currentData(),
                priority=self.filter_priority.currentData(),
                apartment_id=self.filter_apartment.currentData(),
            )

            self.table.setRowCount(0)
            for i in issues:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(str(i.id)))
                self.table.setItem(row, 1, QTableWidgetItem(i.title))

                loc = f"M. {i.apartment.number}" if i.apartment else (i.location_description or "Część wspólna")
                self.table.setItem(row, 2, QTableWidgetItem(loc))

                pri_item = QTableWidgetItem(i.priority)
                if i.priority == "pilny":
                    pri_item.setForeground(Qt.GlobalColor.red)
                    pri_item.setFont(self._get_bold_font())
                elif i.priority == "wysoki":
                    pri_item.setForeground(Qt.GlobalColor.darkRed)
                self.table.setItem(row, 3, pri_item)

                status_item = QTableWidgetItem(i.status)
                if i.status in ("nowe", "przyjęte"):
                    status_item.setForeground(Qt.GlobalColor.red)
                elif i.status == "w trakcie":
                    status_item.setForeground(Qt.GlobalColor.darkYellow)
                elif i.status == "zakończone":
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                self.table.setItem(row, 4, status_item)

                self.table.setItem(row, 5, QTableWidgetItem(i.reporter_name or "—"))
                self.table.setItem(row, 6, QTableWidgetItem(format_date(i.reported_at)))

                cost = f"{i.estimated_cost:.2f} zł" if i.estimated_cost else "—"
                self.table.setItem(row, 7, QTableWidgetItem(cost))

            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować usterek:\n{e}")

    def _get_bold_font(self):
        font = self.font()
        font.setBold(True)
        return font

    def _get_selected_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(self.table.item(selected[0].row(), 0).text())

    def add_issue(self):
        try:
            session = get_session()
            dialog = IssueDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                IssueService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać usterki:\n{e}")

    def edit_issue(self):
        i_id = self._get_selected_id()
        if not i_id:
            QMessageBox.information(self, "Informacja", "Zaznacz usterkę do edycji.")
            return

        try:
            session = get_session()
            issue = IssueService.get_by_id(session, i_id)
            if issue:
                dialog = IssueDialog(self, issue)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    IssueService.update(session, i_id, **data)
                    self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się edytować usterki:\n{e}")

    def delete_issue(self):
        i_id = self._get_selected_id()
        if not i_id:
            QMessageBox.information(self, "Informacja", "Zaznacz usterkę do usunięcia.")
            return

        reply = QMessageBox.question(
            self, "Potwierdzenie",
            "Czy na pewno chcesz usunąć to zgłoszenie?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_session()
                IssueService.delete(session, i_id)
                session.close()
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć usterki:\n{e}")
