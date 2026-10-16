from dataclasses import dataclass
from enum import Enum
from math import hypot
from typing import Optional


class PetState(str, Enum):
	IDLE = "idle"
	WANDERING = "wandering"
	BORED = "bored"


Point = tuple[int, int]


@dataclass
class PetModel:
	name: str = "Pet"
	state: PetState = PetState.IDLE
	last_interaction: float = 0.0
	last_cursor_position: Optional[Point] = None
	cursor_still_since: float = 0.0

	bored_after: float = 60.0
	cursor_still_after: float = 30.0

	def interact(self, now: float) -> None:
		self.state = PetState.IDLE
		self.last_interaction = now

	def set_wandering(self) -> None:
		if self.state != PetState.BORED:
			self.state = PetState.WANDERING

	def tick(self, now: float, cursor_position: Point) -> bool:
		if cursor_position != self.last_cursor_position:
			self.last_cursor_position = cursor_position
			self.cursor_still_since = now

		if self.state != PetState.BORED and now - self.last_interaction >= self.bored_after:
			self.state = PetState.BORED
			self.cursor_still_since = now

		if self.state == PetState.BORED and now - self.cursor_still_since >= self.cursor_still_after:
			self.state = PetState.IDLE
			self.last_interaction = now
			return True

		return False


def clamp_position(
	position: Point,
	pet_size: Point,
	screen_origin: Point,
	screen_size: Point,
) -> Point:
	x, y = position
	pet_width, pet_height = pet_size
	screen_x, screen_y = screen_origin
	screen_width, screen_height = screen_size

	max_x = screen_x + max(0, screen_width - pet_width)
	max_y = screen_y + max(0, screen_height - pet_height)
	return max(screen_x, min(x, max_x)), max(screen_y, min(y, max_y))


def move_toward(
	position: Point,
	target: Point,
	distance: int,
) -> Point:
	if distance <= 0:
		return position

	delta_x = target[0] - position[0]
	delta_y = target[1] - position[1]
	length = hypot(delta_x, delta_y)
	if length == 0 or length <= distance:
		return target

	scale = distance / length
	return round(position[0] + delta_x * scale), round(position[1] + delta_y * scale)
