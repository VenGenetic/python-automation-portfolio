# File Organizer Automation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A Python script that automatically organizes files in a directory by moving them to category-specific folders.

## Features

- **Automatic categorization**: Files are sorted into predefined categories (Images, Documents, Audio, etc.)
- **Duplicate handling**: Automatically renames files if duplicates exist
- **Dry run mode**: Test the organization without making actual changes
- **Detailed logging**: Comprehensive logs of all operations
- **Statistics reporting**: Summary of files processed and organized

## Installation

No external dependencies required! Just run the script with Python 3.8+.

## Usage

```bash
# Organize the current directory
python src/organizer.py

# Organize a specific directory
python src/organizer.py /path/to/directory

# Dry run (simulate without making changes)
python src/organizer.py --dry-run