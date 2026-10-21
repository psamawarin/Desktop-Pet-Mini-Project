# Checks and decisions


## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R2 — naming | The application starts and the pet has no saved name | user enters a name and saves it | The name is saved to a local JSON file | Pass `test_storage.py` tests, and manually confirmed by renaming pet |
| C2 / R1 — screen boundary | The pet is at the right or bottom edge of the visible screen. | The pet attempts to wander | The pet stays within the visible boundary and does not wander out | Pass, supported by `test_pet_logic.py` boundary tests |
| C3 / R3 - bored state | The pet is `idle` and there hasn't been a click or a hover for 1 minute | The inactivity timer expires | The state changes to `bored` | Pass, supported by bored state tests in `test_pet_logic.py` |
| C4 / R3 - run to cursor | The pet is `bored` and the mouse has not moved for 30 seconds | The cursor inactivity timer expires | The pet moves toward the cursor and then returns to `idle` | Pass, manually confirmed that the pet moves towards the cursor when timer runs out. `test_pet_logic.py` test confirm the bored timer event and return to idle |


## Two review decisions
- Plan decision: Copilot suggested adding a hunger and needs system but it was excluded to focus on the required states and animation. The wandering behavior uses randomly selected destinations rather than completely random movement.
- Code decision: The planned `pet.py` was implemented as `pet_logic.py` which keep pet state logic. Instead of having a single `test_pet.py`, the tests were expanded to `test_animation.py`, `test_pet_logic.py` and `test_storage.py` to test each aspect seperately.


## Automated tests
- Test file and behaviour checked: `test_animation.py`, `test_pet_logic.py` and `test_storage.py`
- Command I ran: python -m unittest discover
- Final result: All 22 tests pass with no errors.
- Correction and rerun, if needed: None needed.

## Realistic use and final judgment
- Task I tried: Started the application, named the pet, clicked and hovered over the pet, observed the pet wandering and waited for pet to enter bored state.
- Outcome: The name entered was saved to `pet.json`, pet wandered within the screen boundary, click and hover starts the correct animation and after timer runs out a bored pet runs towards the cursor before returning to `idle` state.
- Judgment: Done. The requirements R1-R3 were implemented and tested with tests and manually.
- Remaining limitation or unfinished work: Animation quality could be improved but it does not affect R1-R3.