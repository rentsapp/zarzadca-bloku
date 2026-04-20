import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

def get_icon(icon_name: str) -> QIcon:
    """Returns a QIcon loaded from the assets/icons folder."""
    # Build absolute path relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "assets", "icons", f"{icon_name}.svg")
    
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()
