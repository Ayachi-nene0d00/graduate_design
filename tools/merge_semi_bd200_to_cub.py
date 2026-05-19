import argparse
import os
import shutil
from pathlib import Path

BASE_DIR = r"F:\Python-program\111"
CUB_ROOT = Path(BASE_DIR) / "bird_species_raw" / "CUB_200_2011"
CUB_IMAGES_DIR = CUB_ROOT / "images"
SEMI_IMAGES_DIR = Path(BASE_DIR) / "bird_species_raw" / "Semi-BD200" / "Semi-BD200"

CLASSES_TXT = CUB_ROOT / "classes.txt"
IMAGES_TXT = CUB_ROOT / "images.txt"
LABELS_TXT = CUB_ROOT / "image_class_labels.txt"

VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def read_nonempty_lines(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def get_last_id(lines):
    return int(lines[-1].split()[0]) if lines else 0


def parse_existing_suffixes():
    suffixes = set()
    for name in sorted(os.listdir(CUB_IMAGES_DIR)):
        folder = CUB_IMAGES_DIR / name
        if not folder.is_dir() or "." not in name:
            continue
        suffixes.add(name.split(".", 1)[1])
    return suffixes


def collect_images(folder: Path):
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS]
    return sorted(files, key=lambda p: p.name.lower())


def merge(dry_run=False, limit=None):
    if not CUB_IMAGES_DIR.exists():
        raise FileNotFoundError(f"Missing CUB images dir: {CUB_IMAGES_DIR}")
    if not SEMI_IMAGES_DIR.exists():
        raise FileNotFoundError(f"Missing Semi-BD200 dir: {SEMI_IMAGES_DIR}")

    classes_lines = read_nonempty_lines(CLASSES_TXT)
    images_lines = read_nonempty_lines(IMAGES_TXT)

    next_class_id = get_last_id(classes_lines) + 1
    next_image_id = get_last_id(images_lines) + 1

    existing_suffixes = parse_existing_suffixes()
    semi_class_names = sorted(
        name for name in os.listdir(SEMI_IMAGES_DIR) if (SEMI_IMAGES_DIR / name).is_dir()
    )
    if limit is not None:
        semi_class_names = semi_class_names[:limit]

    to_add = [name for name in semi_class_names if name not in existing_suffixes]

    print(f"CUB classes (before): {len(classes_lines)}")
    print(f"Semi classes found: {len(semi_class_names)}")
    print(f"Semi classes to add: {len(to_add)}")
    print(f"Dry run: {dry_run}")

    if not to_add:
        print("Nothing to merge.")
        return

    new_class_lines = []
    new_image_lines = []
    new_label_lines = []

    added_images = 0
    skipped_empty = 0

    for latin_name in to_add:
        src_dir = SEMI_IMAGES_DIR / latin_name
        dst_folder_name = f"{next_class_id}.{latin_name}"
        dst_dir = CUB_IMAGES_DIR / dst_folder_name

        img_files = collect_images(src_dir)
        if not img_files:
            skipped_empty += 1
            print(f"[warn] no images in class: {latin_name}")
            continue

        if not dry_run:
            if dst_dir.exists():
                raise FileExistsError(f"Target class folder already exists: {dst_dir}")
            shutil.copytree(src_dir, dst_dir)

        new_class_lines.append(f"{next_class_id} {dst_folder_name}")

        for img_path in img_files:
            rel_path = f"{dst_folder_name}/{img_path.name}"
            new_image_lines.append(f"{next_image_id} {rel_path}")
            new_label_lines.append(f"{next_image_id} {next_class_id}")
            next_image_id += 1
            added_images += 1

        next_class_id += 1

    print(f"Classes added: {len(new_class_lines)}")
    print(f"Images added: {added_images}")
    print(f"Empty classes skipped: {skipped_empty}")

    if dry_run:
        print("Dry run finished. No files were changed.")
        return

    with CLASSES_TXT.open("a", encoding="utf-8") as f:
        for line in new_class_lines:
            f.write(line + "\n")

    with IMAGES_TXT.open("a", encoding="utf-8") as f:
        for line in new_image_lines:
            f.write(line + "\n")

    with LABELS_TXT.open("a", encoding="utf-8") as f:
        for line in new_label_lines:
            f.write(line + "\n")

    print("Merge completed and metadata files updated.")


def main():
    parser = argparse.ArgumentParser(description="Merge Semi-BD200 classes into CUB-200_2011 dataset")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--limit", type=int, default=None, help="Only process first N Semi classes (for testing)")
    args = parser.parse_args()

    merge(dry_run=args.dry_run, limit=args.limit)


if __name__ == "__main__":
    main()

