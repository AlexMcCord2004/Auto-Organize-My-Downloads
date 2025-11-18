import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse

# Map of category -> list of file extensions
EXTENSION_MAP = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".java", ".c", ".cpp", ".html", ".css"],
    "Installers": [".exe", ".msi", ".dmg"],
}

LOG_FILENAME = ".downloads_organizer_log"


def get_category(ext: str) -> str:
    for category, exts in EXTENSION_MAP.items():
        if ext.lower() in exts:
            return category
    return "Other"


def organize_downloads(downloads_path: Path, log_path: Path):
    """
    Move files in downloads_path into categorized folders.
    Every move is logged so it can be undone later.
    """
    run_id = datetime.now().isoformat(timespec="seconds")

    # Make sure log file exists
    log_path.touch(exist_ok=True)

    moved_any = False
    with log_path.open("a", encoding="utf-8") as log_file:
        for item in downloads_path.iterdir():
            if item.is_file() and item.name != LOG_FILENAME:
                ext = item.suffix
                category = get_category(ext)
                target_dir = downloads_path / category
                target_dir.mkdir(exist_ok=True)

                new_path = target_dir / item.name
                if new_path.exists():
                    stamped_name = f"{new_path.stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}{new_path.suffix}"
                    new_path = target_dir / stamped_name

                shutil.move(str(item), str(new_path))
                moved_any = True

                # Log format: run_id|from_path|to_path
                log_file.write(f"{run_id}|{item.resolve()}|{new_path.resolve()}\n")
                print(f"Moved {item.name} -> {new_path.relative_to(downloads_path)}")

    if not moved_any:
        print("Nothing to organize — your Downloads folder is already clean.")


def undo_last_run(downloads_path: Path, log_path: Path):
    """
    Undo the last run by moving files back to their original locations
    based on the log file.
    """
    if not log_path.exists():
        print("No log file found. Nothing to undo.")
        return

    with log_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("Log is empty. Nothing to undo.")
        return

    last_run_id = lines[-1].split("|", 1)[0]

    last_run_entries = []
    remaining_entries = []

    for line in lines:
        run_id, src_str, dst_str = line.split("|", 2)
        if run_id == last_run_id:
            last_run_entries.append((run_id, Path(src_str), Path(dst_str)))
        else:
            remaining_entries.append(line)

    if not last_run_entries:
        print("No entries for the last run. Nothing to undo.")
        return

    # Undo in reverse order to be safe
    for _, src_path, dst_path in reversed(last_run_entries):
        if dst_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dst_path), str(src_path))
            try:
                print(f"Restored {dst_path.name} -> {src_path}")
            except ValueError:
                print(f"Restored {dst_path} -> {src_path}")
        else:
            print(f"Skipped {dst_path} (file no longer exists).")

    # Rewrite log without the undone run
    with log_path.open("w", encoding="utf-8") as f:
        for line in remaining_entries:
            f.write(line + "\n")

    print("Undo complete for the last run.")


def main():
    home = Path.home()
    default_downloads = home / "Downloads"

    parser = argparse.ArgumentParser(
        description="Organize your Downloads folder into categorized subfolders."
    )
    parser.add_argument(
        "--downloads",
        type=str,
        default=str(default_downloads),
        help="Path to the Downloads folder (default: ~/Downloads)",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last organize operation.",
    )

    args = parser.parse_args()
    downloads_path = Path(args.downloads).expanduser()
    log_path = downloads_path / LOG_FILENAME

    if not downloads_path.exists():
        print(f"Downloads path does not exist: {downloads_path}")
        return

    if args.undo:
        undo_last_run(downloads_path, log_path)
    else:
        organize_downloads(downloads_path, log_path)


if __name__ == "__main__":
    main()
