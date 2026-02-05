from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectstaticCommand
from django.core.management.base import CommandError


class Command(CollectstaticCommand):
    def handle(self, *args, **options):
        if not options.get("dry_run"):
            self.stdout.write(self.style.NOTICE("Building frontend assets..."))
            frontend_dir = Path(settings.BASE_DIR) / "frontend"
            if not frontend_dir.exists():
                raise CommandError(f"Frontend directory not found: {frontend_dir}")

            npm = shutil.which("npm")
            if not npm:
                raise CommandError("npm not found. Install Node.js to build assets.")

            try:
                subprocess.run([npm, "run", "build:css"], cwd=frontend_dir, check=True)
            except subprocess.CalledProcessError as exc:
                raise CommandError("Frontend build failed.") from exc

        return super().handle(*args, **options)
