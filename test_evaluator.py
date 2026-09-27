from analyzer.codebase_analyzer import analyze_codebase
from evaluation.documentation_evaluator import calculate_basic_metrics


CODEBASE_FOLDER = "input/legacy_project"


# Analyze the legacy codebase
codebase = analyze_codebase(
    CODEBASE_FOLDER
)


# For this test, assume all detected
# code elements have documentation.
documented_items = []


for file_data in codebase:

    # Add functions
    for function in file_data["functions"]:

        documented_items.append({
            "name": function["name"],
            "documentation": "Generated documentation"
        })


    # Add class methods
    for class_info in file_data["classes"]:

        for method in class_info["methods"]:

            documented_items.append({
                "name": method["name"],
                "documentation": "Generated documentation"
            })


# Calculate metrics
metrics = calculate_basic_metrics(
    codebase,
    documented_items
)


print("\n================================")
print("     DOCUMENTATION EVALUATION")
print("================================")

print(
    f"\nTotal code elements: "
    f"{metrics['total_code_elements']}"
)

print(
    f"Documented elements: "
    f"{metrics['documented_elements']}"
)

print(
    f"Documentation completeness: "
    f"{metrics['documentation_completeness']:.2f}%"
)