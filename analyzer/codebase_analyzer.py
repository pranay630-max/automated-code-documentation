from analyzer.file_scanner import get_python_files
from analyzer.ast_analyzer import analyze_python_file


def analyze_codebase(folder):

    python_files = get_python_files(folder)

    codebase = []

    for file_path in python_files:

        print(
            f"Analyzing: {file_path}"
        )

        result = analyze_python_file(
            file_path
        )

        codebase.append(result)

    return codebase