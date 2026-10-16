# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
Write the first two expectations before implementation. Fill in actual results after running them.

| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R2 — naming | The application starts and the pet has no saved name | user enters a name and saves it | The name is saved to a local JSON file | Not tested yet |
| C2 / R1 — screen boundary | The pet is at the right or bottom edge of the visible screen. | The pet attempts to wander | The pet stayes within the visible boundary and does not wander out | Not tested yet |
| C3 / R3 - bored state | The pet is `idle` and there hasn't been a click or a hover for 1 minute | The inactivity timers expires | The state changes to `bored` | Not tested yet |
| C4 / R3 - cursor movement | The pet is `bored` and the mouse has not moved for 30 seconds | The cursor inactivity timer expires | The pet moves toward the cursor and then returns to `idle` | Not tested yet |


## Two review decisions
- Plan decision: [What I accepted or changed, and why. One or two sentences.]
- Code decision: [File/function/component, what I accepted or changed, and why. One or two sentences.]

## Automated tests
- Test file and behaviour checked: [...]
- Command I ran: [...]
- Final result: [Actual test count and outcome.]
- Correction and rerun, if needed: [Brief account, or None needed.]

## Realistic use and final judgment
- Task I tried: [One realistic use from start to finish.]
- Outcome: [What happened and whether it served the intended user/purpose.]
- Judgment: [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work: [One specific item, or a useful next check.]