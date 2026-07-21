"""
Модальное окно отзывов о закупке
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QFrame, QRadioButton,
                             QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_dialog_styles


class ReviewDialog(QDialog):
    """Диалог оставления отзыва о закупке"""

    def __init__(self, request_id, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.rating = 5  # По умолчанию 5 звёзд

        self.setWindowTitle("Отзыв о закупке")
        self.setFixedSize(600, 500)
        self.setModal(True)

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # Заголовок
        header = QHBoxLayout()
        header.setSpacing(Spacing.SM)

        icon = create_icon_label(IconNames.STAR, size=32)
        header.addWidget(icon)

        title = QLabel("Отзыв о закупке")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        header.addWidget(title)
        header.addStretch()

        layout.addLayout(header)

        subtitle = QLabel(f"Заявка #{self.request_id}")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)

        # Оценка
        rating_card = QFrame()
        rating_card.setObjectName("formCard")
        rating_layout = QVBoxLayout(rating_card)
        rating_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        rating_layout.setSpacing(Spacing.SM)

        rating_title = QLabel("Ваша оценка")
        rating_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        rating_layout.addWidget(rating_title)

        stars_layout = QHBoxLayout()
        stars_layout.setSpacing(Spacing.SM)

        self.rating_group = QButtonGroup()
        for i in range(1, 6):
            star_radio = QRadioButton("⭐")
            star_radio.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_XLARGE))
            star_radio.setChecked(i == self.rating)
            star_radio.toggled.connect(lambda checked, val=i: self.on_rating_changed(val))
            self.rating_group.addButton(star_radio)
            stars_layout.addWidget(star_radio)

        stars_layout.addStretch()
        rating_layout.addLayout(stars_layout)

        self.rating_label = QLabel("Отлично!")
        self.rating_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        self.rating_label.setStyleSheet(f"color: {Colors.SUCCESS};")
        rating_layout.addWidget(self.rating_label)

        layout.addWidget(rating_card)

        # Текстовый отзыв
        review_card = QFrame()
        review_card.setObjectName("formCard")
        review_layout = QVBoxLayout(review_card)
        review_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        review_layout.setSpacing(Spacing.SM)

        review_title = QLabel("Комментарий")
        review_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        review_layout.addWidget(review_title)

        self.review_text = QTextEdit()
        self.review_text.setPlaceholderText("Расскажите о качестве товаров, скорости доставки, соответствии описанию...")
        self.review_text.setFixedHeight(150)
        self.review_text.setObjectName("inputField")
        review_layout.addWidget(self.review_text)

        layout.addWidget(review_card)

        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(Spacing.SM)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        cancel_btn.setFixedSize(120, Sizes.BUTTON_HEIGHT)
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)

        submit_btn = QPushButton("Отправить отзыв")
        submit_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        submit_btn.setFixedSize(200, Sizes.BUTTON_HEIGHT)
        submit_btn.setObjectName("saveButton")
        submit_btn.clicked.connect(self.submit_review)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(submit_btn)

        layout.addLayout(buttons_layout)

    def on_rating_changed(self, rating):
        """Изменение оценки"""
        self.rating = rating
        labels = {1: "Плохо", 2: "Ниже среднего", 3: "Средне", 4: "Хорошо", 5: "Отлично!"}
        colors = {1: Colors.DANGER, 2: Colors.WARNING, 3: Colors.TEXT_SECONDARY, 4: Colors.PRIMARY, 5: Colors.SUCCESS}

        self.rating_label.setText(labels.get(rating, ""))
        self.rating_label.setStyleSheet(f"color: {colors.get(rating, Colors.TEXT_PRIMARY)};")

    def submit_review(self):
        """Отправка отзыва"""
        review_text = self.review_text.toPlainText().strip()

        if not review_text:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Внимание", "Пожалуйста, напишите комментарий!")
            return

        # TODO: Сохранить отзыв в БД
        print(f"Отзыв для заявки #{self.request_id}:")
        print(f"Оценка: {self.rating}/5")
        print(f"Комментарий: {review_text}")

        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Успех", "Спасибо за ваш отзыв!")
        self.accept()

    def apply_styles(self):
        self.setStyleSheet(get_dialog_styles())