from analyzer.codebase_analyzer import analyze_codebase
from llm.semantic_analyzer import generate_documentation
from generator.documentation_generator import create_documentation


CODEBASE_FOLDER = "input/legacy_project"

codebase = analyze_codebase(CODEBASE_FOLDER)

documented_items = []


print("\n========================================")
print("       LLM CODEBASE DOCUMENTATION")
print("========================================")


for file_data in codebase:

    file_path = file_data["file"]

    print(f"\nProcessing file: {file_path}")

    # -----------------------------
    # Document functions
    # -----------------------------

    for function in file_data["functions"]:

        print(
            f"  Analyzing function: "
            f"{function['name']}"
        )

        documentation = generate_documentation(
            function["code"]
        )

        documented_items.append({
          "name": function["name"],
          "type": "function",
          "file": file_path,
          "code": function["code"],
          "documentation": documentation
      })


    # -----------------------------
    # Document classes and methods
    # -----------------------------

    for class_info in file_data["classes"]:

        print(
            f"  Analyzing class: "
            f"{class_info['name']}"
        )

        for method in class_info["methods"]:

            print(
                f"    Analyzing method: "
                f"{method['name']}"
            )

            documentation = generate_documentation(
                method["code"]
            )

            documented_items.append({
              "name": method["name"],
              "type": "method",
              "class": class_info["name"],
              "file": file_path,
              "code": method["code"],
              "documentation": documentation
            })


# -----------------------------
# Generate final documentation
# -----------------------------

create_documentation(
    documented_items,
    "output/documentation.md"
)

print("\n========================================")
print("Documentation generation completed!")
print("Output: output/documentation.md")
print("========================================")