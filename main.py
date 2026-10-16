import sys
import signal
import time
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QInputDialog

from pet_logic import PetEvent, PetModel, PetState
from pet_window import PetWindow
from storage import load_name, save_name

DATA_PATH = Path(__file__).with_name("pet.json")


def main() -> int:
	app = QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(False)
	pet = PetModel(name=load_name(DATA_PATH))

	window = PetWindow(pet)
	window.move_clamped((200, 200))
	window.show()

	def rename_pet() -> None:
		name, accepted = QInputDialog.getText(
			window,
			"Name your pet",
			"Pet name:",
			text=pet.name,
		)
		if accepted and name.strip():
			window.set_name(name)
			save_name(DATA_PATH, pet.name)

	window.on_rename = rename_pet
	rename_pet()

	def interact() -> None:
		pet.interact(time.monotonic())
		window.update()

	window.on_interaction = interact

	timer = QTimer(window)
	last_tick = time.monotonic()
	chasing_cursor = False

	def update_pet() -> None:
		nonlocal chasing_cursor, last_tick
		now = time.monotonic()
		dt = max(0.0, now - last_tick)
		last_tick = now
		cursor = QCursor.pos()
		event = pet.tick(now, (cursor.x(), cursor.y()))
		if event == PetEvent.GAVE_UP:
			chasing_cursor = True
			window.set_chasing_cursor(True)
		if chasing_cursor:
			# Keep chasing across timer ticks instead of moving only once.
			chasing_cursor = not window.move_toward_cursor(dt)
			if not chasing_cursor:
				window.set_chasing_cursor(False)
		elif pet.state == PetState.WANDERING:
			window.wander_step(dt)
		elif (
			pet.state == PetState.IDLE
			and pet.last_interaction is not None
			and now - pet.last_interaction >= 2
		):
			pet.set_wandering()
		window.update()

	timer.timeout.connect(update_pet)
	timer.start(500)

	signal.signal(signal.SIGINT, lambda *_: app.quit())
	return app.exec()


if __name__ == "__main__":
	raise SystemExit(main())
