"""
Project Archival & Packaging Script.
Creates a complete standalone distribution ZIP file of the project.
"""

import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DOWNLOADS_DIR = os.path.dirname(PARENT_DIR)
ZIP_OUTPUT_PATH = os.path.join(PARENT_DIR, "AI_Environmental_Intelligence_Full_Project.zip")
ZIP_OUTPUT_DOWNLOADS = os.path.join(DOWNLOADS_DIR, "AI_Environmental_Intelligence_Fixed.zip")

EXCLUDE_DIRS = {"venv", ".git", "__pycache__", ".pytest_cache", ".vscode", ".idea"}
EXCLUDE_EXTS = {".pyc", ".pyo"}

def create_project_zip():
    print(f"Creating project ZIP archive at:\n -> {ZIP_OUTPUT_PATH}")
    file_count = 0

    with zipfile.ZipFile(ZIP_OUTPUT_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTS or file.endswith(".log"):
                    continue

                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, BASE_DIR)
                arcname = os.path.join("AI_Environmental_Intelligence", rel_path)

                zipf.write(abs_path, arcname)
                file_count += 1

    size_mb = os.path.getsize(ZIP_OUTPUT_PATH) / (1024 * 1024)
    print(f"Successfully packaged {file_count} files into ZIP archive ({size_mb:.2f} MB).")

    import shutil
    try:
        shutil.copy2(ZIP_OUTPUT_PATH, ZIP_OUTPUT_DOWNLOADS)
        print(f"Also copied archive to:\n -> {ZIP_OUTPUT_DOWNLOADS}")
    except Exception as e:
        print(f"Note: Could not copy to {ZIP_OUTPUT_DOWNLOADS}: {e}")

if __name__ == "__main__":
    create_project_zip()
