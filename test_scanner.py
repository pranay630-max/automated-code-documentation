from analyzer.file_scanner import get_python_files


folder = "input/legacy_project"

files = get_python_files(folder)

print("\n===== PYTHON FILES FOUND =====")

for file in files:
    print("-", file)

print(f"\nTotal Python files: {len(files)}")