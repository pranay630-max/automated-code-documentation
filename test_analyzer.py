from analyzer.ast_analyzer import analyze_python_file


file_path = "input/legacy_project/calculator.py"

result = analyze_python_file(file_path)


print("\n===== CODE ANALYSIS =====")

print("\nFile:")
print(result["file"])


print("\nFunctions:")

for function in result["functions"]:

    parameters = ", ".join(function["parameters"])

    print(
        f"\nFunction: {function['name']}"
    )

    print(
        f"Parameters: {parameters}"
    )

    print(
        f"Line: {function['line']}"
    )

    print("\nSource Code:")
    print(function["code"])


print("\nClasses:")

for class_info in result["classes"]:
    print(
        f"- {class_info['name']} "
        f"[Line {class_info['line']}]"
    )


print("\nImports:")

for import_name in result["imports"]:
    print("-", import_name)