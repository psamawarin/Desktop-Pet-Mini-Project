import sys
import time
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QInputDialog

from pet_logic import PetModel, PetState
from pet_window import PetWindow
from storage import load_name, save_name


DATA_PATH = Path(__file__).with_name("pet.json")


def main() -> int:
	app = QApplication(sys.argv)
	pet = PetModel(name=load_name(DATA_PATH), last_interaction=time.monotonic())

	window = PetWindow(pet)
	window.move_clamped((200, 200))
	window.show()

	name, accepted = QInputDialog.getText(
		window,
		"Name your pet",
		"Pet name:",
		text=pet.name,
	)
	if accepted and name.strip():
		window.set_name(name)
		save_name(DATA_PATH, pet.name)

	def interact() -> None:
		pet.interact(time.monotonic())
		window.update()

	window.on_interaction = interact

	timer = QTimer(window)

	def update_pet() -> None:
		now = time.monotonic()
		cursor = QCursor.pos()
		moved_to_cursor = pet.tick(now, (cursor.x(), cursor.y()))
		if moved_to_cursor:
			window.move_toward_cursor()
		elif pet.state == PetState.WANDERING:
			window.wander_step()
		elif pet.state == PetState.IDLE and now - pet.last_interaction >= 2:
			pet.set_wandering()
		window.update()

	timer.timeout.connect(update_pet)
	timer.start(500)

	return app.exec()


if __name__ == "__main__":
	raise SystemExit(main())
