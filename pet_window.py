import random
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QTimer, QRect, Qt
from PySide6.QtGui import (
    QAction,
    QCursor,
    QGuiApplication,
    QImage,
    QPainter,
    QPixmap,
    QTransform,
)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QMenu, QWidget

from animation import frame_paths
from pet_logic import FPoint, PetModel, PetState, clamp_position, step_toward, to_pixels


class PetWindow(QWidget):
    def __init__(self, pet: PetModel, on_interaction: Optional[Callable[[], None]] = None):
        super().__init__()
        self.pet = pet
        self.on_interaction = on_interaction
        self.position: FPoint = (0.0, 0.0)
        self.setFixedSize(96, 96)
        asset_dir = Path(__file__).resolve().parent / "assets"
        self.animation_frames = {
            animation_name: [
                self._load_pet_image(asset_path)
                for asset_path in frame_paths(asset_dir, animation_name)
            ]
            for animation_name in ("idle", "walking_left", "bored")
        }
        self._animation_key: Optional[tuple[str, bool]] = None
        self._active_frames: list[QPixmap] = []
        self._frame_index = 0
        self._walking_left = True
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setToolTip(self.pet.name)
        self.wander_target: Optional[FPoint] = None

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._advance_animation)
        self.animation_timer.start(200)

    def _load_pet_image(self, asset_path: Path) -> QPixmap:
        if asset_path.suffix.lower() == ".svg":
            image = QImage(self.size(), QImage.Format.Format_ARGB32_Premultiplied)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            renderer = QSvgRenderer(str(asset_path))
            if not renderer.isValid():
                painter.end()
                raise ValueError(f"Pet image is not a valid SVG: {asset_path}")
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

    def _animation_name(self) -> str:
        if self.pet.state == PetState.BORED:
            return "bored"
        if self.pet.state == PetState.WANDERING:
            return "walking_left"
        return "idle"

    def _ensure_animation(self) -> None:
        animation_name = self._animation_name()
        animation_key = (animation_name, self._walking_left)
        if animation_key == self._animation_key:
            return

        frames = self.animation_frames[animation_name]
        if animation_name == "walking_left" and not self._walking_left:
            frames = [
                frame.transformed(
                    QTransform().scale(-1, 1),
                    Qt.TransformationMode.SmoothTransformation,
                )
                for frame in frames
            ]
        self._active_frames = frames
        self._animation_key = animation_key
        self._frame_index = 0

    def _advance_animation(self) -> None:
        self._ensure_animation()
        self._frame_index = (self._frame_index + 1) % len(self._active_frames)
        self.update()

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
        previous_position = self.position
        screen = self.screen_rect()
        self.position = clamp_position(
            position,
            (self.width(), self.height()),
            (screen.x(), screen.y()),
            (screen.width(), screen.height()),
        )
        self.move(*to_pixels(self.position))
        if self.pet.state == PetState.WANDERING and self.position[0] != previous_position[0]:
            self._walking_left = self.position[0] < previous_position[0]
            self._ensure_animation()

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
        self._ensure_animation()
        painter = QPainter(self)
        pet_image = self._active_frames[self._frame_index]
        image_x = (self.width() - pet_image.width()) // 2
        image_y = (self.height() - pet_image.height()) // 2
        painter.drawPixmap(image_x, image_y, pet_image)