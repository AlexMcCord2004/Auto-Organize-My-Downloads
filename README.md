# Downloads Organizer

A simple Python automation script that organizes your **Downloads** folder by sorting files into category folders (Images, Documents, Archives, Code, Installers, etc.).  
It also includes an **undo feature** that restores all files moved during the last run.

---

## Features
- Automatically sorts files by extension  
- Creates category folders if needed  
- Prevents overwriting (adds timestamp when needed)  
- **Undo last run** using a log file  
- No external libraries required  

---

## How to Use

### 1. Clone the project
```bash

git clone https://github.com/<your-username>/downloads-organizer
cd downloads-organizer

#2. Run the organizer

This scans your ~/Downloads folder and sorts files into subfolders.

python src/organizer.py

#3. To undo last run
python src/organizer.py --undo

