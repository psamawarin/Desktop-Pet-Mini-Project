from dataclasses import dataclass
from enum import Enum
from math import floor, hypot
from typing import Optional


class PetState(str, Enum):
	IDLE = "idle"
	WANDERING = "wandering"
	BORED = "bored"


class PetEvent(str, Enum):
	BECAME_BORED = "became_bored"
	GAVE_UP = "gave_up"


FPoint = tuple[float, float]

@dataclass
class PetModel:
	name: str = "Pet"
	state: PetState = PetState.IDLE
	last_interaction: Optional[float] = None
	last_cursor_position: Optional[FPoint] = None
	cursor_still_since: Optional[float] = None

	bored_after: float = 60.0
	cursor_still_after: float = 30.0

	def interact(self, now: float) -> None:
		self.set_idle()
		self.last_interaction = now

	def set_idle(self) -> None:
		self.state = PetState.IDLE

	def set_wandering(self) -> None:
		if self.state == PetState.IDLE:
			self.state = PetState.WANDERING

	def tick(self, now: float, cursor_position: FPoint) -> Optional[PetEvent]:
		if self.last_interaction is None:
			self.last_interaction = now

		if cursor_position != self.last_cursor_position:
			self.last_cursor_position = cursor_position
			self.cursor_still_since = now

		if self.state != PetState.BORED and now - self.last_interaction >= self.bored_after:
			self.state = PetState.BORED
			self.cursor_still_since = now
			return PetEvent.BECAME_BORED

		if (
			self.state == PetState.BORED
			and self.cursor_still_since is not None
			and now - self.cursor_still_since >= self.cursor_still_after
		):
			self.set_idle()
			self.last_interaction = now
			return PetEvent.GAVE_UP

		return None


def clamp_position(
	position: FPoint,
	pet_size: FPoint,
	screen_origin: FPoint,
	screen_size: FPoint,
) -> FPoint:
	x, y = position
	pet_width, pet_height = pet_size
	screen_x, screen_y = screen_origin
	screen_width, screen_height = screen_size

	max_x = screen_x + max(0, screen_width - pet_width)
	max_y = screen_y + max(0, screen_height - pet_height)
	return max(screen_x, min(x, max_x)), max(screen_y, min(y, max_y))


def move_toward(position: FPoint, target: FPoint, distance: float) -> FPoint:
	if distance <= 0:
		return position
	dx, dy = target[0] - position[0], target[1] - position[1]
	length = hypot(dx, dy)
	if length <= distance:
		return target
	s = distance / length
	return position[0] + dx * s, position[1] + dy * s


def step_toward(position: FPoint, target: FPoint, speed: float, dt: float) -> FPoint:
	return move_toward(position, target, max(0.0, speed * dt))


def to_pixels(position: FPoint) -> tuple[int, int]:
	return tuple(floor(value + 0.5) for value in position)