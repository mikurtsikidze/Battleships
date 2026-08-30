from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


PROJECT_ROOT = Path(__file__).resolve().parent


class RestartHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.process: subprocess.Popen | None = None
        self.start_game()

    def start_game(self) -> None:
        if self.process is not None:
            self.process.terminate()
            self.process.wait()

        print("\nStarting game...\n")

        self.process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=PROJECT_ROOT,
        )

    def on_modified(self, event) -> None:
        if event.is_directory:
            return

        if not event.src_path.endswith(".py"):
            return

        if Path(event.src_path).resolve() == Path(__file__).resolve():
            return

        print(
            f"\nFile changed: {event.src_path}"
        )

        self.start_game()


def main() -> None:
    handler = RestartHandler()

    observer = Observer()

    observer.schedule(
        handler,
        str(PROJECT_ROOT),
        recursive=True,
    )

    observer.start()

    print(
        "Watching project files..."
    )

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()