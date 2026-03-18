from pathlib import Path
from settings import IMAGES_DIR, MUSIC_DIR, FONTS_DIR, MAPS_DIR


def _resolve_case_insensitive(directory: Path, filename: str) -> Path:
    target = filename.lower()
    for path in directory.iterdir():
        if path.name.lower() == target:
            return path
    raise FileNotFoundError(f"Could not find asset '{filename}' in {directory}")


def image_path(filename: str) -> str:
    return str(_resolve_case_insensitive(IMAGES_DIR, filename))


def music_path(filename: str) -> str:
    return str(_resolve_case_insensitive(MUSIC_DIR, filename))


def font_path(filename: str) -> str:
    return str(_resolve_case_insensitive(FONTS_DIR, filename))


def map_path(filename: str) -> str:
    return str(_resolve_case_insensitive(MAPS_DIR, filename))
