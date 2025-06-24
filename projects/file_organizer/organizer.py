import os
import shutil
import logging
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# File categories with their corresponding extensions
FILE_CATEGORIES = {
    'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'tiff'],
    'Documents': ['pdf', 'docx', 'doc', 'txt', 'xlsx', 'pptx', 'md', 'rtf', 'odt', 'csv'],
    'Audio': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a'],
    'Video': ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'mpeg', 'webm'],
    'Archives': ['zip', 'rar', 'tar', 'gz', '7z', 'iso', 'dmg'],
    'Code': ['py', 'js', 'html', 'css', 'java', 'c', 'cpp', 'json', 'xml', 'php', 'rb', 'swift'],
    'Executables': ['exe', 'msi', 'bat', 'sh', 'app', 'apk', 'jar'],
    'Design': ['psd', 'ai', 'xd', 'fig', 'sketch', 'eps'],
    'Data': ['db', 'sqlite', 'sql', 'csv', 'tsv'],
    'Others': []  # For unknown extensions
}


def get_category(extension: str) -> str:
    """Determine the file category based on its extension

    Args:
        extension: File extension without the dot

    Returns:
        Category name or 'Others' if not found
    """
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'


def organize_files(directory: str, dry_run: bool = False) -> dict:
    """Organize files in the specified directory

    Args:
        directory: Path of the directory to organize
        dry_run: If True, only shows what would be done without making changes

    Returns:
        Dictionary with operation statistics
    """
    stats = {category: 0 for category in FILE_CATEGORIES}
    stats['total'] = 0
    stats['skipped'] = 0

    logger.info(f"🚀 Starting organization of: {directory}")

    # Create category directories if they don't exist
    for category in FILE_CATEGORIES:
        category_path = os.path.join(directory, category)
        if not dry_run and not os.path.exists(category_path):
            os.makedirs(category_path, exist_ok=True)
            logger.info(f"📁 Created category folder: {category}")

    # Process files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories and the log file
        if os.path.isdir(file_path) or filename == 'file_organizer.log':
            continue

        # Get file extension
        _, extension = os.path.splitext(filename)
        extension = extension[1:]  # Remove the dot

        # Determine category
        category = get_category(extension)

        # Handle files without extension
        if not extension:
            category = 'Others'
            logger.warning(f"⚠️ No extension found for file: {filename}")

        # Build destination path
        dest_path = os.path.join(directory, category, filename)

        # Handle duplicate files
        counter = 1
        while os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            new_filename = f"{base}_{counter}{ext}"
            dest_path = os.path.join(directory, category, new_filename)
            counter += 1

        # Move the file (or simulate in dry run)
        if dry_run:
            logger.info(f"📋 [DRY RUN] Would move: {filename} -> {category}/")
        else:
            try:
                shutil.move(file_path, dest_path)
                logger.info(f"✅ Moved: {filename} -> {category}/")
            except Exception as e:
                logger.error(f"❌ Failed to move {filename}: {e}")
                stats['skipped'] += 1
                continue

        stats[category] += 1
        stats['total'] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Automatically organize files in a directory by their type',
        epilog='Example: python organizer.py "C:\\Users\\ferna\\Downloads" --dry-run'
    )
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory to organize (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simulate organization without making changes')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Organize subdirectories recursively')

    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        logger.error(f"❌ Invalid directory: {args.directory}")
        return

    # Organize files
    start_time = datetime.now()

    # Single directory organization
    if not args.recursive:
        stats = organize_files(args.directory, args.dry_run)
    else:
        # Recursive organization
        stats = {category: 0 for category in FILE_CATEGORIES}
        stats['total'] = 0
        stats['skipped'] = 0

        for root, dirs, files in os.walk(args.directory):
            # Skip category folders
            if any(folder in FILE_CATEGORIES for folder in root.split(os.sep)):
                continue

            logger.info(f"\n🔍 Processing directory: {root}")
            dir_stats = organize_files(root, args.dry_run)

            # Aggregate statistics
            for key, value in dir_stats.items():
                if key in stats:
                    stats[key] += value

    duration = datetime.now() - start_time

    # Show summary
    logger.info("\n📊 Organization Summary:")
    logger.info(f"  Directory: {args.directory}")
    logger.info(f"  Total files processed: {stats['total']}")
    logger.info(f"  Files skipped: {stats['skipped']}")

    if not args.dry_run:
        logger.info("\n🗂️ Files organized by category:")
        for category, count in stats.items():
            if category not in ['total', 'skipped'] and count > 0:
                logger.info(f"  {category}: {count} files")

    logger.info(f"⏱️  Operation completed in {duration.total_seconds():.2f} seconds")
    logger.info("✨ Organization complete!")


if __name__ == "__main__":
    main()