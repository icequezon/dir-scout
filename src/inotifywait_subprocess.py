#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
from typing import Generator, Optional
from src.logger import logger

DEFAULT_WATCH_DIR = "/watched"
DEFAULT_EVENTS = ["create", "modify", "delete", "close_write", "moved_to"]


class InotifyWatcher:
    """
    Encapsulates `inotifywait` as a subprocess and exposes filesystem
    events as a generator.
    """

    def __init__(
        self,
        watch_dir: Optional[str] = None,
        include_dotfiles: bool = False,
        events: Optional[list[str]] = None,
    ):
        self.watch_dir = watch_dir or DEFAULT_WATCH_DIR
        self.include_dotfiles = include_dotfiles
        self.events = events or DEFAULT_EVENTS
        self.exclude_pattern = None if include_dotfiles else r"/\.[^/]+$"
        self.process: Optional[subprocess.Popen] = None

    def _build_cmd(self) -> list[str]:
        """Build inotifywait command list."""
        cmd = ["inotifywait", "-m", "-r", "--format", "%w %e %f"]
        for e in self.events:
            cmd += ["-e", e]
        if self.exclude_pattern:
            cmd += ["--exclude", self.exclude_pattern]
        cmd.append(self.watch_dir)
        return cmd

    def start(self):
        """Start inotifywait subprocess."""
        if not Path(self.watch_dir).exists():
            sys.exit(f"[inotify] Directory not found: {self.watch_dir}")

        cmd = self._build_cmd()
        logger.info(f"[inotify] Starting watcher on {self.watch_dir}")
        if self.exclude_pattern:
            logger.info(f"[inotify] Excluding files matching: {self.exclude_pattern}")
        else:
            logger.info("[inotify] Including dotfiles")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # line buffered
        )

    def get_notifications(self) -> Generator[dict, None, None]:
        """
        Yield events as dictionaries:
        {
            "path": str,
            "action": str,
            "filename": str,
            "fullpath": str
        }
        """
        if not self.process or not self.process.stdout:
            raise RuntimeError("Watcher not started. Call .start() first.")

        try:
            for line in self.process.stdout:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(" ", 2)
                if len(parts) != 3:
                    continue

                path, action, filename = parts
                yield {
                    "path": path,
                    "action": action,
                    "file_name": filename,
                    "file_path": os.path.join(path, filename),
                }
        except KeyboardInterrupt:
            logger.info("[inotify] Interrupted, stopping...")
        finally:
            self.stop()

    def stop(self):
        """Gracefully stop the subprocess."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=5)
            logger.info("[inotify] Watcher stopped")
