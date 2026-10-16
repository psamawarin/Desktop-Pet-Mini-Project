import unittest

from pet_logic import (
    PetEvent,
    PetModel,
    PetState,
    clamp_position,
    move_toward,
    step_toward,
    to_pixels,
)


class PetModelTests(unittest.TestCase):
    def test_starts_idle_and_interaction_returns_to_idle(self):
        pet = PetModel()
        pet.set_wandering()

        pet.interact(5.0)

        self.assertEqual(pet.state, PetState.IDLE)
        self.assertEqual(pet.last_interaction, 5.0)

    def test_becomes_bored_after_one_minute_without_interaction(self):
        pet = PetModel()

        self.assertIsNone(pet.tick(60.0, (100, 100)))
        event = pet.tick(120.0, (100, 100))

        self.assertEqual(pet.state, PetState.BORED)
        self.assertEqual(event, PetEvent.BECAME_BORED)

    def test_moves_toward_cursor_after_thirty_seconds_of_boredom(self):
        pet = PetModel()
        pet.tick(0.0, (100, 100))
        pet.tick(60.0, (100, 100))

        event = pet.tick(90.0, (100, 100))

        self.assertEqual(event, PetEvent.GAVE_UP)
        self.assertEqual(pet.state, PetState.IDLE)

    def test_cursor_movement_resets_bored_timer(self):
        pet = PetModel()
        pet.tick(0.0, (100, 100))
        pet.tick(60.0, (100, 100))

        event = pet.tick(89.0, (200, 200))

        self.assertIsNone(event)
        self.assertEqual(pet.state, PetState.BORED)

    def test_bored_pet_cannot_start_wandering(self):
        pet = PetModel()
        pet.tick(0.0, (100, 100))
        pet.tick(60.0, (100, 100))

        pet.set_wandering()

        self.assertEqual(pet.state, PetState.BORED)

    def test_set_idle_stops_wandering(self):
        pet = PetModel()
        pet.set_wandering()

        pet.set_idle()

        self.assertEqual(pet.state, PetState.IDLE)

    def test_interaction_while_bored_returns_to_idle(self):
        pet = PetModel()
        pet.tick(0.0, (100, 100))
        pet.tick(60.0, (100, 100))

        pet.interact(70.00)
        self.assertEqual(pet.state, PetState.IDLE)


class MovementTests(unittest.TestCase):
    def test_clamp_position_keeps_pet_inside_screen(self):
        position = clamp_position(
            (-20, 900),
            (100, 100),
            (0, 0),
            (800, 600),
        )

        self.assertEqual(position, (0, 500))

    def test_clamp_position_supports_screen_origins(self):
        position = clamp_position(
            (4000, 100),
            (100, 100),
            (1920, 0),
            (1280, 1080),
        )

        self.assertEqual(position, (3100, 100))

    def test_move_toward_stops_at_target(self):
        self.assertEqual(move_toward((0, 0), (3, 4), 10), (3, 4))

    def test_move_toward_limits_step_distance(self):
        self.assertEqual(move_toward((0, 0), (100, 0), 25), (25, 0))

    def test_step_toward_uses_speed_per_second(self):
        self.assertEqual(step_toward((0, 0), (100, 0), 20, 0.5), (10, 0))

    def test_to_pixels_rounds_half_up(self):
        self.assertEqual(to_pixels((1.49, 1.5)), (1, 2))
        self.assertEqual(to_pixels((-1.5, -1.51)), (-1, -2))


if __name__ == "__main__":
    unittest.main()