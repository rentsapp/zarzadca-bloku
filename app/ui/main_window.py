"""Główne okno aplikacji z nawigacją boczną."""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from app.utils.icons import get_icon

from app.config import APP_NAME, APP_DESCRIPTION, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.apartments_view import ApartmentsView
from app.ui.views.persons_view import PersonsView
from app.ui.views.payments_view import PaymentsView
from app.ui.views.issues_view import IssuesView
from app.ui.views.building_visualization_view import BuildingVisualizationView
from app.ui.views.reports_view import ReportsView
from app.ui.views.about_view import AboutView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — {APP_DESCRIPTION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel nawigacji
        nav_panel = QWidget()
        nav_panel.setObjectName("nav_panel")
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        title = QLabel(APP_NAME)
        title.setObjectName("app_title")
        nav_layout.addWidget(title)

        subtitle = QLabel(APP_DESCRIPTION)
        subtitle.setObjectName("app_subtitle")
        nav_layout.addWidget(subtitle)

        # Przyciski nawigacji
        self.nav_buttons: list[QPushButton] = []
        nav_items = [
            ("Dashboard", 0, "dashboard"),
            ("Mieszkania", 1, "home"),
            ("Osoby", 2, "users"),
            ("Płatności", 3, "credit-card"),
            ("Usterki", 4, "wrench"),
            ("Wizualizacja", 5, "grid"),
            ("Raporty", 6, "pie-chart"),
            ("O programie", 7, "info"),
        ]

        for text, idx, icon_name in nav_items:
            btn = QPushButton(f"  {text}")
            btn.setIcon(get_icon(icon_name))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self._switch_view(i))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        nav_layout.addStretch()
        main_layout.addWidget(nav_panel)

        # Stos widoków
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.dashboard_view = DashboardView(self)
        self.apartments_view = ApartmentsView(self)
        self.persons_view = PersonsView(self)
        self.payments_view = PaymentsView(self)
        self.issues_view = IssuesView(self)
        self.visualization_view = BuildingVisualizationView(self)
        self.reports_view = ReportsView(self)
        self.about_view = AboutView(self)

        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.apartments_view)
        self.stack.addWidget(self.persons_view)
        self.stack.addWidget(self.payments_view)
        self.stack.addWidget(self.issues_view)
        self.stack.addWidget(self.visualization_view)
        self.stack.addWidget(self.reports_view)
        self.stack.addWidget(self.about_view)

        main_layout.addWidget(self.stack)

        # Domyślnie dashboard
        self._switch_view(0)

    def _switch_view(self, index: int):
        """Przełącza widok i podświetla aktywny przycisk."""
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Odśwież widok po przełączeniu
        widget = self.stack.currentWidget()
        if hasattr(widget, "refresh"):
            widget.refresh()

    def navigate_to(self, view_name: str):
        """Nawigacja z poziomu kodu — np. z dashboardu."""
        mapping = {
            "dashboard": 0, "apartments": 1, "persons": 2,
            "payments": 3, "issues": 4, "visualization": 5,
            "reports": 6, "about": 7,
        }
        idx = mapping.get(view_name, 0)
        self._switch_view(idx)
