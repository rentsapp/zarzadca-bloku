"""Widok dashboardu — ekran startowy z podsumowaniem."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QFrame, QGridLayout, QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.dashboard_service import DashboardService
from app.utils.formatting import format_currency, format_date


class StatCard(QFrame):
    """Karta statystyczna z wartością i etykietą."""
    def __init__(self, value: str, label: str, color: str = "#3b82f6"):
        super().__init__()
        self.setProperty("class", "stat-card")
        self.setObjectName("stat_card")
        self.setStyleSheet(f"""
            QFrame#stat_card {{
                background-color: white;
                border-radius: 14px;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-left: 4px solid {color};
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 28px; font-weight: 700; color: #212121;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        self._value_label = value_label

        text_label = QLabel(label)
        text_label.setStyleSheet("font-size: 12px; color: #757575; font-weight: 500;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        layout.addWidget(text_label)

    def update_value(self, value: str):
        self._value_label.setText(value)


class DashboardView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("dashboard_content")
        content.setStyleSheet("#dashboard_content { background-color: #f4f6f8; }")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Nagłówek
        header = QLabel("Dashboard")
        header.setProperty("class", "view-title")
        header.setStyleSheet("font-size: 20px; font-weight: 700; color: #212121;")
        layout.addWidget(header)

        # Karty statystyczne
        cards_layout = QGridLayout()
        cards_layout.setSpacing(14)

        self.card_total = StatCard("0", "Wszystkie mieszkania", "#43a047")
        self.card_occupied = StatCard("0", "Zamieszkane", "#2e7d32")
        self.card_free = StatCard("0", "Wolne", "#a5d6a7")
        self.card_reserved = StatCard("0", "Zarezerwowane", "#66bb6a")
        self.card_renovation = StatCard("0", "W remoncie", "#e53935")
        self.card_persons = StatCard("0", "Aktywne osoby", "#388e3c")
        self.card_overdue = StatCard("0", "Zaległe płatności", "#ef6c00")
        self.card_debt = StatCard("0 zł", "Suma zaległości", "#c62828")
        self.card_issues = StatCard("0", "Aktywne usterki", "#ff7043")

        cards_layout.addWidget(self.card_total, 0, 0)
        cards_layout.addWidget(self.card_occupied, 0, 1)
        cards_layout.addWidget(self.card_free, 0, 2)
        cards_layout.addWidget(self.card_reserved, 0, 3)
        cards_layout.addWidget(self.card_renovation, 0, 4)
        cards_layout.addWidget(self.card_persons, 1, 0)
        cards_layout.addWidget(self.card_overdue, 1, 1)
        cards_layout.addWidget(self.card_debt, 1, 2)
        cards_layout.addWidget(self.card_issues, 1, 3)

        layout.addLayout(cards_layout)

        # Szybkie akcje
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        btn_add_apt = QPushButton(" Dodaj mieszkanie")
        btn_add_apt.setIcon(get_icon("plus"))
        btn_add_apt.setIconSize(QSize(18, 18))
        btn_add_apt.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_apt.clicked.connect(lambda: self._quick_action("add_apartment"))
        actions_layout.addWidget(btn_add_apt)

        btn_add_person = QPushButton(" Dodaj osobę")
        btn_add_person.setIcon(get_icon("users"))
        btn_add_person.setIconSize(QSize(18, 18))
        btn_add_person.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_person.clicked.connect(lambda: self._quick_action("add_person"))
        actions_layout.addWidget(btn_add_person)

        btn_add_payment = QPushButton(" Dodaj płatność")
        btn_add_payment.setIcon(get_icon("dollar-sign"))
        btn_add_payment.setIconSize(QSize(18, 18))
        btn_add_payment.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_payment.clicked.connect(lambda: self._quick_action("add_payment"))
        actions_layout.addWidget(btn_add_payment)

        btn_add_issue = QPushButton(" Dodaj usterkę")
        btn_add_issue.setIcon(get_icon("wrench"))
        btn_add_issue.setIconSize(QSize(18, 18))
        btn_add_issue.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_issue.clicked.connect(lambda: self._quick_action("add_issue"))
        actions_layout.addWidget(btn_add_issue)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Sekcje tabelaryczne
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)

        # Ostatnie płatności
        pay_section = QVBoxLayout()
        pay_title = QLabel("Ostatnie płatności")
        pay_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #212121;")
        pay_section.addWidget(pay_title)

        self.recent_payments_table = QTableWidget()
        self.recent_payments_table.setColumnCount(5)
        self.recent_payments_table.setHorizontalHeaderLabels(["Mieszkanie", "Okres", "Suma", "Status", "Data"])
        self.recent_payments_table.horizontalHeader().setStretchLastSection(True)
        self.recent_payments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_payments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_payments_table.verticalHeader().setVisible(False)
        pay_section.addWidget(self.recent_payments_table)
        tables_layout.addLayout(pay_section)

        # Ostatnie usterki
        issue_section = QVBoxLayout()
        issue_title = QLabel("Ostatnie usterki")
        issue_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #212121;")
        issue_section.addWidget(issue_title)

        self.recent_issues_table = QTableWidget()
        self.recent_issues_table.setColumnCount(4)
        self.recent_issues_table.setHorizontalHeaderLabels(["Tytuł", "Priorytet", "Status", "Data"])
        self.recent_issues_table.horizontalHeader().setStretchLastSection(True)
        self.recent_issues_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recent_issues_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recent_issues_table.verticalHeader().setVisible(False)
        issue_section.addWidget(self.recent_issues_table)
        tables_layout.addLayout(issue_section)

        layout.addLayout(tables_layout)
        layout.addStretch()

        scroll.setWidget(content)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def refresh(self):
        """Odświeża dane dashboardu."""
        try:
            session = get_session()
            stats = DashboardService.get_stats(session)

            self.card_total.update_value(str(stats["total_apartments"]))
            self.card_occupied.update_value(str(stats["occupied"]))
            self.card_free.update_value(str(stats["free"]))
            self.card_reserved.update_value(str(stats["reserved"]))
            self.card_renovation.update_value(str(stats["renovation"]))
            self.card_persons.update_value(str(stats["active_persons"]))
            self.card_overdue.update_value(str(stats["overdue_count"]))
            self.card_debt.update_value(format_currency(stats["total_debt"]))
            self.card_issues.update_value(str(stats["active_issues"]))

            # Ostatnie płatności
            self.recent_payments_table.setRowCount(0)
            for p in stats["recent_payments"]:
                row = self.recent_payments_table.rowCount()
                self.recent_payments_table.insertRow(row)
                apt_num = p.apartment.number if p.apartment else "—"
                self.recent_payments_table.setItem(row, 0, QTableWidgetItem(apt_num))
                self.recent_payments_table.setItem(row, 1, QTableWidgetItem(f"{p.month:02d}/{p.year}"))
                self.recent_payments_table.setItem(row, 2, QTableWidgetItem(format_currency(p.total_amount)))
                status_item = QTableWidgetItem(p.status)
                if p.status in ("nieopłacone", "po terminie"):
                    status_item.setForeground(Qt.GlobalColor.red)
                elif p.status == "opłacone":
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                self.recent_payments_table.setItem(row, 3, status_item)
                self.recent_payments_table.setItem(row, 4, QTableWidgetItem(format_date(p.due_date)))

            # Ostatnie usterki
            self.recent_issues_table.setRowCount(0)
            for i in stats["recent_issues"]:
                row = self.recent_issues_table.rowCount()
                self.recent_issues_table.insertRow(row)
                self.recent_issues_table.setItem(row, 0, QTableWidgetItem(i.title))
                pri_item = QTableWidgetItem(i.priority)
                if i.priority == "pilny":
                    pri_item.setForeground(Qt.GlobalColor.red)
                elif i.priority == "wysoki":
                    pri_item.setForeground(Qt.GlobalColor.darkRed)
                self.recent_issues_table.setItem(row, 1, pri_item)
                self.recent_issues_table.setItem(row, 2, QTableWidgetItem(i.status))
                self.recent_issues_table.setItem(row, 3, QTableWidgetItem(format_date(i.reported_at)))

            session.close()
        except Exception as e:
            print(f"Błąd odświeżania dashboardu: {e}")

    def _quick_action(self, action: str):
        """Obsługa szybkich akcji na dashboardzie."""
        if action == "add_apartment":
            self.main_window.navigate_to("apartments")
            self.main_window.apartments_view.add_apartment()
        elif action == "add_person":
            self.main_window.navigate_to("persons")
            self.main_window.persons_view.add_person()
        elif action == "add_payment":
            self.main_window.navigate_to("payments")
            self.main_window.payments_view.add_payment()
        elif action == "add_issue":
            self.main_window.navigate_to("issues")
            self.main_window.issues_view.add_issue()
