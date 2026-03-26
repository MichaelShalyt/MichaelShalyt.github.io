"""Source paths for rebuilding the site from the WordPress export."""

from pathlib import Path

# ROOT_DIRECTORY stores the repository root that contains the export and generated site.
ROOT_DIRECTORY = Path(__file__).resolve().parents[1]

# EXPORT_DIRECTORY stores the folder created from the WordPress export package.
EXPORT_DIRECTORY = ROOT_DIRECTORY / "Original Website Content"

# MEDIA_LIBRARY_DIRECTORY stores the local images and documents exported from WordPress.
MEDIA_LIBRARY_DIRECTORY = EXPORT_DIRECTORY / "Media Library"
