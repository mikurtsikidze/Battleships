# Battleships Project Context

## Project
Desktop Battleships game written in Python.

## Technology
- Python
- PySide6
- Git
- Virtual environment (.venv)

## Current Project Structure

```text
battleships/
├── main.py
├── requirements.txt
├── .gitignore
├── PROJECT_PLAN.md
├── PROJECT_CONTEXT.md
│
├── game/
├── ui/
├── ai/
├── resources/
│   ├── images/
│   └── sounds/
└── tests/


Game Rules
Each player has a 10x10 board.
Ships are placed horizontally or vertically.
Players take turns shooting.
Hit, miss, and sunk ships are tracked.
The winner is the player who destroys all enemy ships.
Current Status
Project setup completed.
Virtual environment created.
PySide6 installed.
Main application created.
Main window created.
Game logic not started yet.
Important Development Rules
Do not put the entire game in one file.
Keep game logic separate from UI.
Work one step at a time.
Do not break existing functionality.
For a new file, provide the complete file.
For an existing file, provide only the necessary change.
Before adding new files or code, check PROJECT_PLAN.md.
After completing a task, update PROJECT_PLAN.md.
Update this file when an important architectural or technical decision is made.
Current Next Step

Build the player and enemy game boards.