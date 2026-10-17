# Implementation plan

This plan records the project-specific steps used to implement R1–R3.

## Steps
1. Create project files:
    - `main.py` starts the PySide6 application.
    - `pet_logic.py` contains the pet model, state transitions, timers, and movement calculations.
    - `pet_window.py` displays the transparent desktop pet and handle mouse events.
    - `animation.py` loads and validates animation frames.
    - `storage.py` saves and loads pet's name using JSON.
    - `test_pet_logic.py`, `test_animation.py`, and `test_storage.py` test the non-GUI logic and storage behavior.

2. Implement R2 by allowing users to set a pet name and save it to a local JSON file. Clicking the pet or moving the cursor into its window returns it to the `idle` state.

3. Implement R1 by moving the pet window across the desktop and checking the screen geometry before each movement. The pet must remain inside the visible screen boundaries.

4. Implement R3 using the movement system from R1. Use `idle`, `wandering`, and `bored` states:
   - No click or hover for 1 minute changes the state to `bored`.
   - While bored, 30 seconds without mouse movement makes the pet move toward the cursor.
   - After moving toward the cursor, the pet returns to `idle`.
   - A click or hover also returns the pet to `idle`.

5. Test the state transitions, animation frame loading, storage, and boundary calculations with `python -m unittest discover`, then launch the application and test naming, wandering, boredom, and cursor movement manually.

## Later changes, if any
1. The planned `pet.py` module was implemented as `pet_logic.py` so the state model and movement calculations remain separate from the PySide6 interface.
2. `animation.py` was added to load and validate the animation frames used by the pet window.
3. The single planned `test_pet.py` was replaced with focused tests: `test_pet_logic.py` for core logic, `test_animation.py` for animation loading, and `test_storage.py` for saving the pet name to local JSON.
4. Timing is handled by `PetModel.tick(now, cursor_position)` in `pet_logic.py`; the GUI supplies the current time and cursor position.