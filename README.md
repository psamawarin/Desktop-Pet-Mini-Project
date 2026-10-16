# Desktop Pet

> This file explains who the project is for, what it should do, and how to run it.

## Purpose
A small Python application for users to interact with a virtual pet on their desktop. 

## Requirements
- R1: The pet moves around the desktop without leaving the visible screen boundaries.
- R2: Hovering over or clicking the pet triggers an interaction, such as a message, movement, or mood change, and the user can give the pet a name.
- R3: The pet has three states: `idle`, `wandering`, and `bored`.
  - It switches between `idle` and `wandering`.
  - After 1 minute without a click or hover, it becomes `bored`.
  - While bored, if the mouse has not moved for 30 seconds, it moves toward the cursor and returns to `idle`.
  - A click or hover returns it to `idle`.

## Setup and use
- Prerequisites: Python 3.11 or newer
- Setup:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install PySide6
```
- Run: Execute `python main.py`.
- Run tests: Execute `python -m unittest`.

## Author and acknowledgements
- Name / student ID: Samawarin Phakdeewanit 6681338
- AI tools used: Copilot
- External code/resources: 

See PLAN.md for the implementation plan and EVIDENCE.md for results and decisions.