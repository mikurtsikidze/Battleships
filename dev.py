from __future__ import annotations

import subprocess
import sys
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


PROJECT_ROOT = Path(__file__).resolve().parent


class RestartHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()

        self.process: subprocess.Popen | None = None
        self.restart_lock = threading.Lock()
        self.restart_pending = False

        self.start_game()

    def start_game(self) -> None:
        with self.restart_lock:
            if self.process is not None:
                if self.process.poll() is None:
                    self.process.terminate()

                    try:
                        self.process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                        self.process.wait()

            print("\nStarting game...\n")

            self.process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=PROJECT_ROOT,
            )

            self.restart_pending = False

    def on_modified(self, event) -> None:
        if event.is_directory:
            return

        if not event.src_path.endswith(".py"):
            return

        if Path(event.src_path).resolve() == Path(__file__).resolve():
            return

        with self.restart_lock:
            if self.restart_pending:
                return

            self.restart_pending = True

        print(
            f"\nFile changed: {event.src_path}"
        )

        threading.Thread(
            target=self._delayed_restart,
            daemon=True,
        ).start()

    def _delayed_restart(self) -> None:
        time.sleep(0.3)
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

        if handler.process is not None:
            handler.process.terminate()

    observer.join()


if __name__ == "__main__":
    main()