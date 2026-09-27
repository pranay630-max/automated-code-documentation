from analyzer.codebase_analyzer import analyze_codebase
from llm.semantic_analyzer import generate_documentation
from evaluation.documentation_validator import validate_documentation


CODEBASE_FOLDER = "input/legacy_project"


print("\n========================================")
print("       DOCUMENTATION VALIDATOR TEST")
print("========================================")


# Analyze codebase
codebase = analyze_codebase(
    CODEBASE_FOLDER
)


for file_data in codebase:

    for function in file_data["functions"]:

        print(
            f"\nChecking: "
            f"{function['name']}"
        )

        documentation = generate_documentation(
            function["code"]
        )

        result = validate_documentation(
            function["code"],
            documentation,
            function["parameters"]
        )

        print(
            f"Status: {result['status']}"
        )

        print(
            f"Issues found: "
            f"{result['issue_count']}"
        )

        for issue in result["issues"]:

            print(
                f"  ⚠ {issue}"
            )


    for class_info in file_data["classes"]:

        for method in class_info["methods"]:

            print(
                f"\nChecking: "
                f"{class_info['name']}."
                f"{method['name']}"
            )

            documentation = generate_documentation(
                method["code"]
            )

            result = validate_documentation(
                method["code"],
                documentation,
                method["parameters"]
            )

            print(
                f"Status: {result['status']}"
            )

            print(
                f"Issues found: "
                f"{result['issue_count']}"
            )

            for issue in result["issues"]:

                print(
                    f"  ⚠ {issue}"
                )


print("\n========================================")
print("       VALIDATOR TEST COMPLETE")
print("========================================")