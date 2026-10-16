# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to R1–R3 rather than copying the requirements here.

## Steps
1. Create project files:
    - `main.py` starts the PySide6 application.
    - `pet.py` contains pet's name, state transitions and timer.
    - `pet_window.py` displays the transparent desktop pet and handle mouse events.
    - `storage.py` saves and loads pet's name using JSON.
    - `test_pet.py` tests pet logic without opening GUI.

2. Implement R2 by allowing users to set a pet name and save it to a local JSON file. Clicking the pet or moving the cursor into its window returns it to the `idle` state.

3. Implement R1 by moving the pet window across the desktop and checking the screen geometry before each movement. The pet must remain inside the visible screen boundaries.

4. Implement R3 using the movement system from R1. Use `idle`, `wandering`, and `bored` states:
   - No click or hover for 1 minute changes the state to `bored`.
   - While bored, 30 seconds without mouse movement makes the pet move toward the cursor.
   - After moving toward the cursor, the pet returns to `idle`.
   - A click or hover also returns the pet to `idle`.

5. Test the state transitions and boundary calculations with `python -m unittest discover`, then launch the application and test naming, wandering, boredom, and cursor movement manually.

## Later changes, if any
