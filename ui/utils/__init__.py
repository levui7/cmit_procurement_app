# PyQt6 основные импорты
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QSpinBox, QDoubleSpinBox, QDateEdit,
    QComboBox, QMessageBox, QTextEdit, QDialog, QScrollArea,
    QFormLayout, QRadioButton, QButtonGroup, QCheckBox,
    QLineEdit, QGroupBox, QStackedWidget, QMainWindow,
    QFileDialog, QProgressBar, QApplication
)

from PyQt6.QtCore import (
    Qt, QDate, QDateTime, QTimer, QThread, pyqtSignal,
    QObject, QSize, QRect, QPoint, QUrl, QFile, QTextStream
)

from PyQt6.QtGui import (
    QFont, QPixmap, QIcon, QColor, QBrush, QPen,
    QPainter, QImage, QPalette, QCursor
)

# Стандартные библиотеки
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple, Union
import json
import sys
import os

# # Наши модули
# from utils.config import *
# from utils.paths import *
# from utils.icons import *