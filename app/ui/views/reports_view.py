"""Widok raportów i eksportu danych do CSV."""

import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QFileDialog, QMessageBox,
    QGroupBox, QHeaderView
)
from PySide6.QtCore import Qt, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.report_service import ReportService
from app.services.apartment_service import ApartmentService
from app.utils.formatting import format_currency, format_date
from app.utils.exporters import export_to_csv


class ReportsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Lewa kolumna: Zestawienia tabelaryczne (QTableWidget proste)
        left_layout = QVBoxLayout()
        header = QLabel("Raporty i Zestawienia")
        header.setProperty("class", "view-title")
        left_layout.addWidget(header)

        # 1. Zadłużenie
        debt_group = QGroupBox("Mieszkania z zadłużeniem")
        debt_layout = QVBoxLayout(debt_group)
        self.debt_table = QTableWidget()
        self.debt_table.setColumnCount(4)
        self.debt_table.setHorizontalHeaderLabels(["Nr Mieszkania", "Klatka", "Piętro", "Zaległość"])
        self.debt_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.debt_table.verticalHeader().setVisible(False)
        self.debt_table.setMinimumHeight(120)
        debt_layout.addWidget(self.debt_table)
        left_layout.addWidget(debt_group)

        # 2. Aktywne usterki
        issue_group = QGroupBox("Aktywne usterki")
        issue_layout = QVBoxLayout(issue_group)
        self.issue_table = QTableWidget()
        self.issue_table.setColumnCount(4)
        self.issue_table.setHorizontalHeaderLabels(["Tytuł", "Data zgłoszenia", "Priorytet", "Status"])
        self.issue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.issue_table.verticalHeader().setVisible(False)
        self.issue_table.setMinimumHeight(120)
        issue_layout.addWidget(self.issue_table)
        left_layout.addWidget(issue_group)

        # 3. Statusy mieszkań (drobne podsumowanie)
        status_group = QGroupBox("Podsumowanie statusów mieszkań")
        status_layout = QVBoxLayout(status_group)
        self.status_table = QTableWidget()
        self.status_table.setColumnCount(2)
        self.status_table.setHorizontalHeaderLabels(["Status", "Liczba"])
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.status_table.verticalHeader().setVisible(False)
        self.status_table.setMinimumHeight(100)
        status_layout.addWidget(self.status_table)
        left_layout.addWidget(status_group, stretch=1)

        layout.addLayout(left_layout, stretch=2)

        # Prawa kolumna: Eksport CSV i akcje
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 35, 0, 0)

        export_group = QGroupBox("Eksport Danych (CSV)")
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(15)

        lbl_desc = QLabel("Wybierz dane, które chcesz wyeksportować do arkusza kalkulacyjnego (Excel, Calc):")
        lbl_desc.setWordWrap(True)
        export_layout.addWidget(lbl_desc)

        btn_export_apts = QPushButton(" Eksportuj wszystkie mieszkania")
        btn_export_apts.setIcon(get_icon("download"))
        btn_export_apts.setIconSize(QSize(18, 18))
        btn_export_apts.clicked.connect(self._export_apartments)
        export_layout.addWidget(btn_export_apts)

        btn_export_debt = QPushButton(" Eksportuj listę zaległości")
        btn_export_debt.setIcon(get_icon("download"))
        btn_export_debt.setIconSize(QSize(18, 18))
        btn_export_debt.clicked.connect(self._export_debts)
        export_layout.addWidget(btn_export_debt)

        btn_export_issues = QPushButton(" Eksportuj aktywne usterki")
        btn_export_issues.setIcon(get_icon("download"))
        btn_export_issues.setIconSize(QSize(18, 18))
        btn_export_issues.clicked.connect(self._export_issues)
        export_layout.addWidget(btn_export_issues)

        export_layout.addStretch()

        right_layout.addWidget(export_group)

        btn_refresh = QPushButton(" Odśwież widok")
        btn_refresh.setIcon(get_icon("refresh"))
        btn_refresh.setIconSize(QSize(18, 18))
        btn_refresh.setProperty("class", "secondary")
        btn_refresh.clicked.connect(self.refresh)
        right_layout.addWidget(btn_refresh)
        right_layout.addStretch()

        layout.addLayout(right_layout, stretch=1)

    def refresh(self):
        try:
            session = get_session()

            # Zadłużenie
            debts = ReportService.apartments_with_debt(session)
            self.debt_table.setRowCount(0)
            for d in debts:
                r = self.debt_table.rowCount()
                self.debt_table.insertRow(r)
                self.debt_table.setItem(r, 0, QTableWidgetItem(d["apartment_number"]))
                self.debt_table.setItem(r, 1, QTableWidgetItem(d["staircase"]))
                self.debt_table.setItem(r, 2, QTableWidgetItem(str(d["floor"])))
                
                amount = QTableWidgetItem(format_currency(d["debt"]))
                amount.setForeground(Qt.GlobalColor.red)
                self.debt_table.setItem(r, 3, amount)

            # Usterki
            issues = ReportService.active_issues(session)
            self.issue_table.setRowCount(0)
            for i in issues:
                r = self.issue_table.rowCount()
                self.issue_table.insertRow(r)
                self.issue_table.setItem(r, 0, QTableWidgetItem(i.title))
                self.issue_table.setItem(r, 1, QTableWidgetItem(format_date(i.reported_at)))
                
                pri = QTableWidgetItem(i.priority)
                if i.priority in ("pilny", "wysoki"):
                    pri.setForeground(Qt.GlobalColor.red)
                self.issue_table.setItem(r, 2, pri)
                self.issue_table.setItem(r, 3, QTableWidgetItem(i.status))

            # Statusy
            stats = ReportService.apartments_by_status(session)
            self.status_table.setRowCount(0)
            for s in stats:
                r = self.status_table.rowCount()
                self.status_table.insertRow(r)
                self.status_table.setItem(r, 0, QTableWidgetItem(s["status"].capitalize()))
                self.status_table.setItem(r, 1, QTableWidgetItem(str(s["count"])))

            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować raportów:\n{e}")

    def _get_save_path(self, default_name: str) -> str:
        desk = os.path.join(os.path.expanduser("~"), "Desktop")
        path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz plik CSV",
            os.path.join(desk, f"{default_name}_{datetime.now().strftime('%Y%m%d')}.csv"),
            "CSV Files (*.csv)"
        )
        return path

    def _export_apartments(self):
        path = self._get_save_path("Mieszkania")
        if not path: return

        try:
            session = get_session()
            apts = ApartmentService.get_all(session)
            session.close()

            headers = ["ID", "Numer", "Klatka", "Piętro", "Metraz", "Pokoje", "Status", "Typ Wlasnosci", "Bazowy Czynsz", "Balkon", "Komorka"]
            rows = [
                [
                    a.id, a.number, a.staircase, a.floor, str(a.area).replace(".", ","),
                    a.rooms, a.status, a.ownership_type, str(a.base_rent).replace(".", ","),
                    "Tak" if a.has_balcony else "Nie", "Tak" if a.has_storage else "Nie"
                ] for a in apts
            ]
            export_to_csv(path, headers, rows)
            QMessageBox.information(self, "Sukces", f"Pomyślnie wyeksportowano dane do:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd eksportu", str(e))

    def _export_debts(self):
        path = self._get_save_path("Zaleglosci")
        if not path: return

        try:
            session = get_session()
            debts = ReportService.apartments_with_debt(session)
            session.close()

            headers = ["Numer Mieszkania", "Klatka", "Pietro", "Kwota Zaleglosci PLN"]
            rows = [
                [
                    d["apartment_number"], d["staircase"], d["floor"], 
                    str(d["debt"]).replace(".", ",")
                ] for d in debts
            ]
            export_to_csv(path, headers, rows)
            QMessageBox.information(self, "Sukces", f"Pomyślnie wyeksportowano dane do:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd eksportu", str(e))

    def _export_issues(self):
        path = self._get_save_path("Usterki_Aktywne")
        if not path: return

        try:
            session = get_session()
            issues = ReportService.active_issues(session)
            session.close()

            headers = ["ID", "Tytul", "Zglaszajacy", "Data", "Priorytet", "Status", "Lokalizacja"]
            rows = []
            for i in issues:
                loc = f"M. {i.apartment.number} (kl. {i.apartment.staircase})" if i.apartment else (i.location_description or "Czesc wspolna")
                rows.append([
                    i.id, i.title, i.reporter_name or "", format_date(i.reported_at),
                    i.priority, i.status, loc
                ])
            
            export_to_csv(path, headers, rows)
            QMessageBox.information(self, "Sukces", f"Pomyślnie wyeksportowano dane do:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd eksportu", str(e))
