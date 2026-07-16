"""
Все стили приложения
"""

# ========== ОБЩИЕ СТИЛИ ==========
COMMON_STYLES = """
    QWidget {
        background-color: #F9FAFB;
    }

    QLabel {
        selection-background-color: transparent;
        selection-color: transparent;
        background-color: transparent;
    }

    QToolTip {
        background-color: #F9FAFB;
        color: #334155;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 12px;
        font-family: 'Segoe UI';
    }

    QPushButton {
        selection-background-color: transparent;
        selection-color: transparent;
        outline: none;
    }
"""

# ========== SIDEBAR ==========
SIDEBAR_STYLES = """
    #sidebar {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    #logoFrame {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E5E7EB;
    }

    #menuFrame {
        background-color: #FFFFFF;
    }

    QPushButton#menuButton {
        background-color: transparent;
        border: none;
        color: #4B5563;
        border-radius: 10px;
        text-align: left;
        padding-left: 20px;
    }

    QPushButton#menuButton:hover {
        background-color: #F3F4F6;
        color: #3B82F6;
    }

    QPushButton#activeMenu {
        background-color: #EFF6FF;
        border: none;
        color: #3B82F6;
        border-radius: 10px;
        text-align: left;
        padding-left: 20px;
        border-left: 4px solid #3B82F6;
        font-weight: bold;
    }
"""

# ========== EXIT CARD ==========
EXIT_CARD_STYLES = """
    #exitCard {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }

    #exitCard:hover {
        border: 2px solid #EF4444;
    }
"""

# ========== ГЛАВНАЯ СТРАНИЦА ==========
MAIN_PAGE_STYLES = """
    #card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
    }

    #card:hover {
        border: 2px solid #3B82F6;
    }
"""

# ========== СТРАНИЦА СОЗДАНИЯ ЗАЯВКИ ==========
CREATE_REQUEST_STYLES = """
    #formCard {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
    }

    #iconContainer {
        background-color: transparent;
        border-radius: 12px;
    }

    #inputField {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px 15px;
        color: #1F2937;
    }

    #inputField:focus {
        border: 2px solid #3B82F6;
    }

    #clearButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }

    #nextButton {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
    }
"""

# ========== СТРАНИЦА ИСТОРИИ ==========
HISTORY_STYLES = """
    #historyCard {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }

    #historyCard:hover {
        border: 2px solid #3B82F6;
    }

    #dateBlock {
        background-color: #F3F4FF;
        border-radius: 8px;
    }

    #openButton {
        background-color: #EFF6FF;
        color: #3B82F6;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
    }

    #exportButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
    }

    #deleteButton {
        background-color: #FFFFFF;
        color: #EF4444;
        border: 1px solid #FECACA;
        border-radius: 6px;
    }

    #backButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }

    #currentPage {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 6px;
    }

    #pageButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
    }

    #navButton {
        background-color: #FFFFFF;
        color: #6B7280;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
    }
"""

# ========== СТРАНИЦА КАТАЛОГА ==========
CATALOG_STYLES = """
    #searchContainer {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }

    #searchInput {
        background-color: transparent;
        border: none;
        padding: 0 5px;
        color: #1F2937;
    }

    #addButton {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
    }

    #importButton, #exportButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }

    #productsTable {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        gridline-color: #E5E7EB;
    }

    #productsTable QHeaderView::section {
        background-color: #F9FAFB;
        color: #6B7280;
        border: none;
        border-bottom: 1px solid #E5E7EB;
        padding: 10px;
        font-weight: bold;
    }

    #editButton {
        background-color: #FFFFFF;
        color: #3B82F6;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
    }
"""

# ========== СТРАНИЦА "О ПРЕДПРИЯТИИ" ==========
ABOUT_STYLES = """
    #infoCard {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
    }

    #directionCard {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }
"""

# ========== СТРАНИЦА НАСТРОЕК (СВЕТЛАЯ ТЕМА) ==========
SETTINGS_LIGHT_STYLES = """
    QWidget#scrollArea {
        background-color: #F9FAFB;
    }

    #mainTitle {
        color: #1F2937;
    }

    #subtitle {
        color: #6B7280;
    }

    #settingsGroup {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }

    #groupTitle {
        color: #1F2937;
    }

    #groupDescription {
        color: #6B7280;
    }

    #groupSeparator {
        background-color: #E5E7EB;
    }

    QRadioButton#themeRadio {
        background-color: transparent;
        color: #374151;
        spacing: 8px;
    }

    QRadioButton#themeRadio::indicator {
        width: 20px;
        height: 20px;
        border-radius: 10px;
        border: 2px solid #D1D5DB;
        background-color: #FFFFFF;
    }

    QRadioButton#themeRadio::indicator:checked {
        border: 2px solid #3B82F6;
        background-color: #3B82F6;
    }

    QCheckBox#settingsCheckbox {
        background-color: transparent;
        color: #374151;
        spacing: 8px;
    }

    QCheckBox#settingsCheckbox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid #D1D5DB;
        background-color: #FFFFFF;
    }

    QCheckBox#settingsCheckbox::indicator:checked {
        background-color: #3B82F6;
        border: 2px solid #3B82F6;
    }

    QComboBox#settingsCombo {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 5px 10px;
        color: #1F2937;
    }

    QSpinBox#settingsSpin {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 5px 10px;
        color: #1F2937;
    }

    QLineEdit#settingsInput {
        background-color: #F9FAFB;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 5px 10px;
        color: #1F2937;
    }

    QPushButton#saveButton {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
    }

    QPushButton#secondaryButton {
        background-color: #FFFFFF;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }

    QPushButton#dangerButton {
        background-color: #FFFFFF;
        color: #EF4444;
        border: 1px solid #FECACA;
        border-radius: 8px;
    }
"""

# ========== СТРАНИЦА НАСТРОЕК (ТЕМНАЯ ТЕМА) ==========
SETTINGS_DARK_STYLES = """
    QWidget#scrollArea {
        background-color: #111827;
    }

    #mainTitle {
        color: #F9FAFB;
    }

    #subtitle {
        color: #9CA3AF;
    }

    #settingsGroup {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 12px;
    }

    #groupTitle {
        color: #F9FAFB;
    }

    #groupDescription {
        color: #9CA3AF;
    }

    #groupSeparator {
        background-color: #374151;
    }

    QRadioButton#themeRadio {
        background-color: transparent;  /* ✅ ДОБАВЛЕНО: прозрачный фон */
        color: #D1D5DB;
    }

    QRadioButton#themeRadio::indicator {
        border: 2px solid #4B5563;
        background-color: #111827;
    }

    QRadioButton#themeRadio::indicator:checked {
        border: 2px solid #3B82F6;
        background-color: #3B82F6;
    }

    QCheckBox#settingsCheckbox {
        background-color: transparent;  /* ✅ ДОБАВЛЕНО: прозрачный фон */
        color: #D1D5DB;
    }

    QCheckBox#settingsCheckbox::indicator {
        border: 2px solid #4B5563;
        background-color: #111827;
    }

    QCheckBox#settingsCheckbox::indicator:checked {
        background-color: #3B82F6;
        border: 2px solid #3B82F6;
    }

    QComboBox#settingsCombo {
        background-color: #111827;
        border: 1px solid #374151;
        color: #F3F4F6;
    }

    QSpinBox#settingsSpin {
        background-color: #111827;
        border: 1px solid #374151;
        color: #F3F4F6;
    }

    QLineEdit#settingsInput {
        background-color: #111827;
        border: 1px solid #374151;
        color: #F3F4F6;
    }

    QPushButton#secondaryButton {
        background-color: #374151;
        color: #F3F4F6;
        border: 1px solid #4B5563;
    }

    QPushButton#dangerButton {
        background-color: #374151;
        color: #FCA5A5;
        border: 1px solid #7F1D1D;
    }
"""


# ========== ФУНКЦИИ ДЛЯ ПРИМЕНЕНИЯ СТИЛЕЙ ==========

def get_main_window_styles():
    """Стили для главного окна (AppWindow)"""
    return COMMON_STYLES + SIDEBAR_STYLES + EXIT_CARD_STYLES


def get_main_page_styles():
    """Стили для главной страницы"""
    return COMMON_STYLES + MAIN_PAGE_STYLES + EXIT_CARD_STYLES


def get_create_request_styles():
    """Стили для страницы создания заявки"""
    return COMMON_STYLES + CREATE_REQUEST_STYLES + EXIT_CARD_STYLES


def get_history_styles():
    """Стили для страницы истории"""
    return COMMON_STYLES + HISTORY_STYLES + EXIT_CARD_STYLES


def get_catalog_styles():
    """Стили для страницы каталога"""
    return COMMON_STYLES + CATALOG_STYLES + EXIT_CARD_STYLES


def get_about_styles():
    """Стили для страницы "О предприятии"""
    return COMMON_STYLES + ABOUT_STYLES + EXIT_CARD_STYLES


def get_settings_styles(theme="light"):
    """Стили для страницы настроек"""
    if theme == "dark":
        return COMMON_STYLES + SETTINGS_DARK_STYLES + EXIT_CARD_STYLES
    return COMMON_STYLES + SETTINGS_LIGHT_STYLES + EXIT_CARD_STYLES