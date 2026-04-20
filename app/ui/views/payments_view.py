"""Widok płatności — tabela z CRUD i filtrami."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox,
    QMessageBox, QHeaderView, QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.payment_service import PaymentService
from app.services.apartment_service import ApartmentService
from app.ui.dialogs.payment_dialog import PaymentDialog
from app.enums import PaymentStatus
from app.utils.formatting import format_currency, format_date


class PaymentsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Płatności i Zaległości")
        header.setProperty("class", "view-title")
        layout.addWidget(header)

        # Panel filtrów
        filter_panel = QWidget()
        filter_panel.setObjectName("filter_panel")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        self.filter_apartment = QComboBox()
        self.filter_apartment.addItem("Wszystkie mieszkania", None)
        filter_layout.addWidget(self.filter_apartment)

        self.filter_status = QComboBox()
        self.filter_status.addItem("Wszystkie statusy", "")
        for s in PaymentStatus:
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
        btn_add.clicked.connect(self.add_payment)
        action_layout.addWidget(btn_add)

        btn_edit = QPushButton(" Edytuj")
        btn_edit.setIcon(get_icon("pencil"))
        btn_edit.setIconSize(QSize(18, 18))
        btn_edit.clicked.connect(self.edit_payment)
        action_layout.addWidget(btn_edit)

        btn_mark_paid = QPushButton(" Oznacz jako opłacone")
        btn_mark_paid.setIcon(get_icon("check-circle"))
        btn_mark_paid.setIconSize(QSize(18, 18))
        btn_mark_paid.setProperty("class", "success")
        btn_mark_paid.clicked.connect(self.mark_as_paid)
        action_layout.addWidget(btn_mark_paid)

        btn_delete = QPushButton(" Usuń")
        btn_delete.setIcon(get_icon("trash"))
        btn_delete.setIconSize(QSize(18, 18))
        btn_delete.setProperty("class", "danger")
        btn_delete.clicked.connect(self.delete_payment)
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
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Mieszkanie", "Miesiąc/Rok", "Suma", "Wpłacono", "Saldo", "Termin", "Zapłacono", "Status"
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
        self.filter_apartment.addItem("Wszystkie mieszkania", None)
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
            print(f"Błąd ładowania mieszkań dla filtra: {e}")

    def _reset_filters(self):
        self.filter_apartment.setCurrentIndex(0)
        self.filter_status.setCurrentIndex(0)
        self.refresh()

    def refresh(self):
        self._update_apartments_combo()
        try:
            session = get_session()
            payments = PaymentService.filter_payments(
                session,
                apartment_id=self.filter_apartment.currentData(),
                status=self.filter_status.currentData(),
            )

            self.table.setRowCount(0)
            for p in payments:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(str(p.id)))
                apt_num = p.apartment.number if p.apartment else "—"
                self.table.setItem(row, 1, QTableWidgetItem(apt_num))
                self.table.setItem(row, 2, QTableWidgetItem(f"{p.month:02d}/{p.year}"))
                self.table.setItem(row, 3, QTableWidgetItem(format_currency(p.total_amount)))
                self.table.setItem(row, 4, QTableWidgetItem(format_currency(p.paid_amount)))

                balance_item = QTableWidgetItem(format_currency(p.balance))
                if p.balance > 0:
                    balance_item.setForeground(Qt.GlobalColor.red)
                    balance_item.setFont(self._get_bold_font())
                self.table.setItem(row, 5, balance_item)

                self.table.setItem(row, 6, QTableWidgetItem(format_date(p.due_date)))
                self.table.setItem(row, 7, QTableWidgetItem(format_date(p.paid_date)))

                status_item = QTableWidgetItem(p.status)
                if p.status in ("nieopłacone", "po terminie"):
                    status_item.setForeground(Qt.GlobalColor.red)
                elif p.status == "opłacone":
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                elif p.status == "częściowo opłacone":
                    status_item.setForeground(Qt.GlobalColor.darkYellow)

                self.table.setItem(row, 8, status_item)

            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować płatności:\n{e}")

    def _get_bold_font(self):
        font = self.font()
        font.setBold(True)
        return font

    def _get_selected_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(self.table.item(selected[0].row(), 0).text())

    def add_payment(self):
        try:
            session = get_session()
            dialog = PaymentDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                PaymentService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać płatności:\n{e}")

    def edit_payment(self):
        p_id = self._get_selected_id()
        if not p_id:
            QMessageBox.information(self, "Informacja", "Zaznacz płatność do edycji.")
            return

        try:
            session = get_session()
            p = PaymentService.get_by_id(session, p_id)
            if p:
                dialog = PaymentDialog(self, p)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    PaymentService.update(session, p_id, **data)
                    self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się edytować płatności:\n{e}")

    def mark_as_paid(self):
        p_id = self._get_selected_id()
        if not p_id:
            QMessageBox.information(self, "Informacja", "Zaznacz płatność.")
            return

        try:
            session = get_session()
            PaymentService.mark_as_paid(session, p_id)
            session.close()
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Oznaczenie nie powiodło się:\n{e}")

    def delete_payment(self):
        p_id = self._get_selected_id()
        if not p_id:
            QMessageBox.information(self, "Informacja", "Zaznacz płatność do usunięcia.")
            return

        reply = QMessageBox.question(
            self, "Potwierdzenie",
            "Czy na pewno chcesz usunąć ten wpis płatności?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                session = get_session()
                PaymentService.delete(session, p_id)
                session.close()
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć płatności:\n{e}")
