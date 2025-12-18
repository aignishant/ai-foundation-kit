import os
import shutil
import glob

DIRS_TO_REMOVE = ["build", "dist", "ai_foundation_kit.egg-info"]
EXTENSIONS = [".py", ".sh", ".yml", ".yaml"]
SKIP_DIRS = {".git", ".venv", ".github"}
SKIP_DIRS_EXACT = {".git", ".venv", "__pycache__"}


def clean_artifacts():
    print("🧹 Cleaning artifacts...")
    for d in DIRS_TO_REMOVE:
        if os.path.exists(d):
            print(f"Removing {d}...")
            shutil.rmtree(d)

    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            p = os.path.join(root, "__pycache__")
            print(f"Removing {p}...")
            shutil.rmtree(p)
            dirs.remove("__pycache__")  # Don't traverse into it


def should_skip_dir(d_name):
    return d_name in SKIP_DIRS_EXACT


def remove_comments_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"⚠️  Skipping binary or non-utf8 file: {file_path}")
        return

    new_lines = []
    is_first_line = True
    modified = False

    for line in lines:
        stripped = line.strip()

        if is_first_line and stripped.startswith("#!"):
            new_lines.append(line)
            is_first_line = False
            continue

        is_first_line = False

        if stripped.startswith("#"):
            modified = True
            continue

        new_lines.append(line)

    if modified:
        print(f"✏️  Removing comments from {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)


def process_files():
    print("📝 Processing files...")
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in EXTENSIONS:
                file_path = os.path.join(root, file)
                remove_comments_from_file(file_path)


if __name__ == "__main__":
    clean_artifacts()
    process_files()
    print("✅ Done.")
