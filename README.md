Downloads Organizer

A simple Python automation script that organizes your Downloads folder by sorting files into category folders (Images, Documents, Archives, Code, Installers, etc.).
It also includes an undo feature that restores all files moved during the last run.

Features

Automatically sorts files by extension

Creates category folders if needed

Prevents overwriting (adds timestamp when needed)

Undo last run using a log file

No external libraries required

How to Use
1. Clone the project
git clone https://github.com/<your-username>/downloads-organizer
cd downloads-organizer

2. Run the organizer

This scans your ~/Downloads folder and sorts files into subfolders.

python src/organizer.py

3. Undo the last run

Restores all files moved during the last organize session.

python src/organizer.py --undo

4. Use a custom Downloads folder (optional)
python src/organizer.py --downloads "path/to/your/folder"

How It Works

The script checks file extensions and assigns each file to a category.

It moves files into category folders inside the Downloads directory.

Every move is logged in:

~/Downloads/.downloads_organizer_log


The --undo flag reads the log and moves everything back to where it started.

Requirements

Python 3.7 or newer

No external packages needed
