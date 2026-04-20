"""Wizualizacja budynku — interaktywna siatka mieszkań."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QFrame, QScrollArea, QPushButton, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, Signal, QSize
from app.utils.icons import get_icon

from app.database import get_session
from app.services.apartment_service import ApartmentService
from app.services.issue_service import IssueService
from app.services.payment_service import PaymentService
from app.ui.dialogs.apartment_dialog import ApartmentDialog
from app.ui.dialogs.payment_dialog import PaymentDialog
from app.ui.dialogs.issue_dialog import IssueDialog


class ApartmentTile(QFrame):
    """Kafel reprezentujący pojedyncze mieszkanie w siatce."""
    clicked = Signal(int)

    def __init__(self, apt_id: int, number: str, rooms: int, status: str):
        super().__init__()
        self.apt_id = apt_id
        self.setFixedSize(90, 90)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        lbl_num = QLabel(number)
        lbl_num.setStyleSheet("font-size: 16px; font-weight: 700; color: #212121;")
        lbl_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_num)

        lbl_rooms = QLabel(f"{rooms} pok.")
        lbl_rooms.setStyleSheet("font-size: 11px; color: #616161;")
        lbl_rooms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_rooms)

        self._set_color_by_status(status)

    def _set_color_by_status(self, status: str):
        colors = {
            "wolne": "#e0e0e0",
            "zamieszkane": "#c8e6c9",
            "zarezerwowane": "#dcedc8",
            "w remoncie": "#ffcdd2",
        }
        bg = colors.get(status, "#eeeeee")
        self.setStyleSheet(f"""
            ApartmentTile {{
                background-color: {bg};
                border: 1.5px solid #bdbdbd;
                border-radius: 12px;
            }}
            ApartmentTile:hover {{
                border: 2px solid #43a047;
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.apt_id)
        super().mousePressEvent(event)


class BuildingVisualizationView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_apt_id = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Lewa strona - wizualizacja
        left_panel = QWidget()
        left_panel.setObjectName("left_panel")
        left_panel.setStyleSheet("#left_panel { background-color: #f4f6f8; }")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(24, 24, 24, 24)
        left_layout.setSpacing(16)

        header_layout = QHBoxLayout()
        header = QLabel("Wizualizacja Budynku")
        header.setProperty("class", "view-title")
        header_layout.addWidget(header)

        btn_refresh = QPushButton(" Odśwież Siatkę")
        btn_refresh.setIcon(get_icon("refresh"))
        btn_refresh.setIconSize(QSize(18, 18))
        btn_refresh.setProperty("class", "secondary")
        btn_refresh.clicked.connect(self.refresh)
        header_layout.addStretch()
        header_layout.addWidget(btn_refresh)
        left_layout.addLayout(header_layout)

        # Legenda
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(15)
        legend_items = [
            ("Wolne", "#e0e0e0"),
            ("Zamieszkane", "#c8e6c9"),
            ("Zarezerwowane", "#dcedc8"),
            ("W remoncie", "#ffcdd2")
        ]
        for text, color in legend_items:
            item = QHBoxLayout()
            box = QFrame()
            box.setFixedSize(16, 16)
            box.setStyleSheet(f"background-color: {color}; border: 1px solid #bdbdbd; border-radius: 4px;")
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size: 11px; color: #616161;")
            item.addWidget(box)
            item.addWidget(lbl)
            legend_layout.addLayout(item)
        legend_layout.addStretch()
        left_layout.addLayout(legend_layout)

        # Obszar siatki (scrollowany)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        self.grid_widget = QWidget()
        self.grid_layout = QVBoxLayout(self.grid_widget)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        scroll.setWidget(self.grid_widget)

        left_layout.addWidget(scroll)
        main_layout.addWidget(left_panel, stretch=2)

        # Prawa strona - panel szczegółów
        self.right_panel = QWidget()
        self.right_panel.setMinimumWidth(300)
        self.right_panel.setMaximumWidth(350)
        self.right_panel.setObjectName("right_panel")
        self.right_panel.setStyleSheet("#right_panel { background-color: white; border-left: 1px solid #e0e0e0; }")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(20, 24, 20, 24)
        right_layout.setSpacing(16)

        self.lbl_details_title = QLabel("Wybierz mieszkanie z siatki")
        self.lbl_details_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #212121;")
        self.lbl_details_title.setWordWrap(True)
        right_layout.addWidget(self.lbl_details_title)

        self.details_content = QLabel("Kliknij kafelek po lewej stronie, aby wyświetlić szczegóły mieszkania, powiązane osoby, status płatności oraz aktywne usterki.")
        self.details_content.setWordWrap(True)
        self.details_content.setStyleSheet("font-size: 13px; color: #616161; line-height: 1.5;")
        self.details_content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        right_layout.addWidget(self.details_content)

        # Przyciski akcji (ukryte do czasu wyboru)
        self.action_buttons = QWidget()
        action_btns_layout = QVBoxLayout(self.action_buttons)
        action_btns_layout.setContentsMargins(0, 0, 0, 0)
        action_btns_layout.setSpacing(10)

        self.btn_edit = QPushButton(" Edytuj mieszkanie")
        self.btn_edit.setIcon(get_icon("pencil"))
        self.btn_edit.setIconSize(QSize(18, 18))
        self.btn_edit.clicked.connect(self._edit_current_apartment)
        action_btns_layout.addWidget(self.btn_edit)

        self.btn_add_payment = QPushButton(" Dodaj płatność")
        self.btn_add_payment.setIcon(get_icon("dollar-sign"))
        self.btn_add_payment.setIconSize(QSize(18, 18))
        self.btn_add_payment.setProperty("class", "success")
        self.btn_add_payment.clicked.connect(self._add_payment_for_current)
        action_btns_layout.addWidget(self.btn_add_payment)

        self.btn_add_issue = QPushButton(" Zgłoś usterkę")
        self.btn_add_issue.setIcon(get_icon("wrench"))
        self.btn_add_issue.setIconSize(QSize(18, 18))
        self.btn_add_issue.setProperty("class", "warning")
        self.btn_add_issue.clicked.connect(self._add_issue_for_current)
        action_btns_layout.addWidget(self.btn_add_issue)

        self.action_buttons.setVisible(False)
        right_layout.addWidget(self.action_buttons)

        right_layout.addStretch()
        main_layout.addWidget(self.right_panel, stretch=1)

    def refresh(self):
        """Odświeża siatkę mieszkań."""
        # Wyczyść stary layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            session = get_session()
            apartments = ApartmentService.get_all(session)

            # Grupuj po klatce i piętrze
            from collections import defaultdict
            grid_data = defaultdict(lambda: defaultdict(list))

            for apt in apartments:
                grid_data[apt.staircase][apt.floor].append(apt)

            # Rysuj klatki
            for staircase in sorted(grid_data.keys()):
                sc_label = QLabel(f"Klatka {staircase}")
                sc_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #2e7d32; margin-top: 20px;")
                self.grid_layout.addWidget(sc_label)

                # Rysuj piętra (od najwyższego do zera, żeby przypominało budynek fizycznie)
                floors = sorted(grid_data[staircase].keys(), reverse=True)
                for floor in floors:
                    floor_widget = QWidget()
                    floor_layout = QHBoxLayout(floor_widget)
                    floor_layout.setContentsMargins(0, 0, 0, 0)
                    floor_layout.setSpacing(10)

                    lbl_floor = QLabel(f"P.{floor}")
                    lbl_floor.setFixedWidth(40)
                    lbl_floor.setStyleSheet("font-weight: 600; color: #757575;")
                    floor_layout.addWidget(lbl_floor)

                    apts = sorted(grid_data[staircase][floor], key=lambda a: a.number)
                    for apt in apts:
                        tile = ApartmentTile(apt.id, apt.number, apt.rooms, apt.status)
                        tile.clicked.connect(self._show_details)
                        floor_layout.addWidget(tile)

                    floor_layout.addStretch()
                    self.grid_layout.addWidget(floor_widget)

            session.close()

            # Jeśli coś jest wybrane, odśwież panel szczegółów
            if self.current_apt_id:
                self._show_details(self.current_apt_id)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować siatki:\n{e}")

    def _show_details(self, apt_id: int):
        self.current_apt_id = apt_id
        try:
            session = get_session()
            apt = ApartmentService.get_by_id(session, apt_id)

            if not apt:
                self.lbl_details_title.setText("Mieszkanie nie istnieje")
                self.action_buttons.setVisible(False)
                session.close()
                return

            self.lbl_details_title.setText(f"Mieszkanie nr {apt.number}")
            self.action_buttons.setVisible(True)

            # Przygotuj tekst szczegółów w HTML
            persons = ApartmentService.get_persons_for_apartment(session, apt_id)
            active_issues_count = IssueService.get_active_for_apartment(session, apt_id)

            # Znajdź najnowszą zaległą płatność
            overdue = (
                session.query(app.models.payment.Payment)
                .filter(app.models.payment.Payment.apartment_id == apt_id)
                .filter(app.models.payment.Payment.status.in_(["nieopłacone", "po terminie", "częściowo opłacone"]))
                .all()
            )
            debt = sum(p.balance for p in overdue)

            persons_html = ""
            if persons:
                persons_html = "<ul>"
                for link in persons:
                    p = link.person
                    star = "⭐" if link.is_primary else "👤"
                    persons_html += f"<li>{star} {p.full_name} ({link.role_in_apartment})</li>"
                persons_html += "</ul>"
            else:
                persons_html = "<p>Brak przypisanych osób</p>"

            debt_text = f"<span style='color: red; font-weight: bold;'>{debt:.2f} zł</span>" if debt > 0 else "<span style='color: green;'>Brak zaległości</span>"
            issues_text = f"<span style='color: red; font-weight: bold;'>{active_issues_count}</span>" if active_issues_count > 0 else "Brak"

            html = f"""
            <h3 style='margin-bottom: 5px; color: #334155;'>Informacje ogólne</h3>
            <table cellpadding='3'>
                <tr><td><b>Klatka:</b></td><td>{apt.staircase}</td></tr>
                <tr><td><b>Piętro:</b></td><td>{apt.floor}</td></tr>
                <tr><td><b>Metraż:</b></td><td>{apt.area} m²</td></tr>
                <tr><td><b>Pokoje:</b></td><td>{apt.rooms}</td></tr>
                <tr><td><b>Status:</b></td><td>{apt.status.capitalize()}</td></tr>
                <tr><td><b>Własność:</b></td><td>{apt.ownership_type.capitalize()}</td></tr>
            </table>

            <h3 style='margin-top: 15px; margin-bottom: 5px; color: #334155;'>Lokatorzy i Właściciele</h3>
            {persons_html}

            <h3 style='margin-top: 15px; margin-bottom: 5px; color: #334155;'>Zobowiązania i Stan</h3>
            <table cellpadding='3'>
                <tr><td><b>Czynsz bazowy:</b></td><td>{apt.base_rent:.2f} zł</td></tr>
                <tr><td><b>Zadłużenie:</b></td><td>{debt_text}</td></tr>
                <tr><td><b>Aktywne usterki:</b></td><td>{issues_text}</td></tr>
            </table>
            """
            self.details_content.setText(html)
            session.close()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się załadować szczegółów:\n{e}")

    def _edit_current_apartment(self):
        if not self.current_apt_id: return
        try:
            session = get_session()
            apt = ApartmentService.get_by_id(session, self.current_apt_id)
            if apt:
                dialog = ApartmentDialog(self, apt)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    del data['building_id']
                    ApartmentService.update(session, self.current_apt_id, **data)
                    self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się edytować mieszkania:\n{e}")

    def _add_payment_for_current(self):
        if not self.current_apt_id: return
        try:
            session = get_session()
            dialog = PaymentDialog(self, apartment_id=self.current_apt_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                PaymentService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać płatności:\n{e}")

    def _add_issue_for_current(self):
        if not self.current_apt_id: return
        try:
            session = get_session()
            dialog = IssueDialog(self, apartment_id=self.current_apt_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                IssueService.add(session, **data)
                self.refresh()
            session.close()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać usterki:\n{e}")

# Importy potrzebne dla query wewnątrz klasy (żeby uniknąć circular imports problemów wyżej)
import app.models.payment
