# Downloads Organizer 🧹

A simple Python automation script that cleans up your `Downloads` folder by
sorting files into subfolders like `Images`, `Documents`, `Archives`, `Code`,
and more.

## Features

- Automatically categorizes files by extension
- Creates folders on the fly (Images, Documents, Archives, Code, Installers, Other)
- Safe: only moves files inside your Downloads folder
- Simple, readable code – great starter automation project

## Setup

```bash

git clone https://github.com/<your-username>/downloads-organizer.git
cd downloads-organizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
