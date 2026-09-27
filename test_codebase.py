from analyzer.codebase_analyzer import analyze_codebase


folder = "input/legacy_project"

codebase = analyze_codebase(folder)


print("\n==============================")
print("      CODEBASE ANALYSIS")
print("==============================")


print(
    f"\nTotal files: {len(codebase)}"
)


for file_data in codebase:

    print("\n------------------------------")

    print(
        "File:",
        file_data["file"]
    )

    print("\nFunctions:")

    for function in file_data["functions"]:

        print(
            f"  - {function['name']}()"
        )

    print("\nClasses:")

    for class_info in file_data["classes"]:

        print(
            f"  - {class_info['name']}()"
        )

        print("    Methods:")

        for method in class_info["methods"]:

            print(
                f"      - {method['name']}()"
            )

    print("\nImports:")

    for import_name in file_data["imports"]:

        print(
            f"  - {import_name}"
        )