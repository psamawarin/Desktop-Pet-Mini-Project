import random
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QAction, QCursor, QGuiApplication, QImage, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QMenu, QWidget

from pet_logic import FPoint, PetModel, PetState, clamp_position, step_toward, to_pixels


class PetWindow(QWidget):
    def __init__(self, pet: PetModel, on_interaction: Optional[Callable[[], None]] = None):
        super().__init__()
        self.pet = pet
        self.on_interaction = on_interaction
        self.position: FPoint = (0.0, 0.0)
        self.setFixedSize(96, 96)
        asset_path = Path(__file__).resolve().parent / "assets" / "pet.svg"
        self.pet_image = self._load_pet_image(asset_path)
        if self.pet_image.isNull():
            raise FileNotFoundError(f"Pet image could not be loaded: {asset_path}")
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setToolTip(self.pet.name)
        self.wander_target: Optional[FPoint] = None

    def _load_pet_image(self, asset_path: Path) -> QPixmap:
        if asset_path.suffix.lower() == ".svg":
            image = QImage(self.size(), QImage.Format.Format_ARGB32_Premultiplied)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            renderer = QSvgRenderer(str(asset_path))
            renderer.render(painter)
            painter.end()
            pixmap = QPixmap.fromImage(image)
        else:
            pixmap = QPixmap(str(asset_path))

        return pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def set_name(self, name: str) -> None:
        self.pet.name = name
        self.setToolTip(name)

    def enterEvent(self, event) -> None:
        self._interact()
        super().enterEvent(event)

    def mousePressEvent(self, event) -> None:
        self._interact()
        super().mousePressEvent(event)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self._quit_application)
        menu.addAction(quit_action)
        menu.exec(event.globalPos())

    def _quit_application(self) -> None:
        application = QGuiApplication.instance()
        if application is not None:
            application.quit()

    def _interact(self) -> None:
        self.wander_target = None
        if self.on_interaction is not None:
            self.on_interaction()
        self.update()

    def screen_rect(self) -> QRect:
        screen = QGuiApplication.screenAt(self.frameGeometry().center())
        if screen is None:
            screen = QGuiApplication.primaryScreen()
        return screen.availableGeometry()

    def move_clamped(self, position: FPoint) -> None:
        screen = self.screen_rect()
        self.position = clamp_position(
            position,
            (self.width(), self.height()),
            (screen.x(), screen.y()),
            (screen.width(), screen.height()),
        )
        self.move(*to_pixels(self.position))

    def wander_step(self, dt: float) -> None:
        if self.pet.state != PetState.WANDERING:
            return

        screen = self.screen_rect()
        max_x = screen.x() + max(0, screen.width() - self.width())
        max_y = screen.y() + max(0, screen.height() - self.height())

        if self.wander_target is None or self.position == self.wander_target:
            self.wander_target = (
                random.uniform(screen.x(), max_x),
                random.uniform(screen.y(), max_y),
            )

        self.move_clamped(
            step_toward(self.position, self.wander_target, 120.0, dt)
        )

    def move_toward_cursor(self, dt: float) -> None:
        cursor = QCursor.pos()
        target = (
            cursor.x() - self.width() // 2,
            cursor.y() - self.height() // 2,
        )
        self.move_clamped(step_toward(self.position, target, 48.0, dt))

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        image_x = (self.width() - self.pet_image.width()) // 2
        image_y = (self.height() - self.pet_image.height()) // 2
        painter.drawPixmap(image_x, image_y, self.pet_image)