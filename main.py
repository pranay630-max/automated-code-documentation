from analyzer.codebase_analyzer import analyze_codebase
from analyzer.dependency_analyzer import analyze_dependencies

from llm.semantic_analyzer import generate_documentation
from llm.project_summary import generate_project_summary

from evaluation.documentation_evaluator import (
    calculate_basic_metrics
)

from evaluation.semantic_evaluator import (
    calculate_semantic_similarity
)

from generator.documentation_generator import (
    create_documentation
)


# ==========================================
# Configuration
# ==========================================

CODEBASE_FOLDER = "input/legacy_project"

OUTPUT_FILE = "output/documentation.md"


# ==========================================
# Main Pipeline
# ==========================================

print("\n========================================")
print("     AUTOMATED CODE DOCUMENTATION")
print("========================================")


# ------------------------------------------
# 1. Analyze Codebase
# ------------------------------------------

print("\n[1/6] Analyzing codebase...")

codebase = analyze_codebase(
    CODEBASE_FOLDER
)

print(
    f"Found {len(codebase)} Python files."
)


# ------------------------------------------
# 2. Analyze Dependencies
# ------------------------------------------

print("\n[2/6] Analyzing dependencies...")

dependency_graph = analyze_dependencies(
    CODEBASE_FOLDER
)

print(
    f"Files: {dependency_graph.number_of_nodes()}"
)

print(
    f"Dependencies: "
    f"{dependency_graph.number_of_edges()}"
)


# ------------------------------------------
# 3. Generate Function Documentation
# ------------------------------------------

print("\n[3/6] Generating documentation...")


documented_items = []


for file_data in codebase:

    file_path = file_data["file"]


    # -----------------------------
    # Functions
    # -----------------------------

    for function in file_data["functions"]:

        print(
            f"  Documenting: "
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
    # Class methods
    # -----------------------------

    for class_info in file_data["classes"]:

        for method in class_info["methods"]:

            print(
                f"  Documenting: "
                f"{class_info['name']}."
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


# ------------------------------------------
# 4. Documentation Evaluation
# ------------------------------------------

print("\n[4/6] Evaluating documentation...")


metrics = calculate_basic_metrics(
    codebase,
    documented_items
)


print(
    f"Documentation completeness: "
    f"{metrics['documentation_completeness']:.2f}%"
)


# ------------------------------------------
# 5. Semantic Evaluation
# ------------------------------------------

print("\n[5/6] Calculating semantic similarity...")


similarities = []


for item in documented_items:

    similarity = calculate_semantic_similarity(
        item["code"],
        item["documentation"]
    )

    similarities.append(
        similarity
    )

    print(
        f"  {item['name']}: "
        f"{similarity:.4f}"
    )


if similarities:

    average_similarity = (
        sum(similarities)
        / len(similarities)
    )

else:

    average_similarity = 0


print(
    f"\nAverage semantic similarity: "
    f"{average_similarity:.4f}"
)


# ------------------------------------------
# 6. Generate Documentation
# ------------------------------------------

print("\n[6/6] Creating Markdown documentation...")


create_documentation(
    documented_items,
    OUTPUT_FILE
)


# ------------------------------------------
# Project Summary
# ------------------------------------------

print("\nGenerating project summary...")


project_summary = generate_project_summary(
    codebase,
    dependency_graph
)


print("\n========================================")
print("             FINAL RESULTS")
print("========================================")


print(
    f"\nFiles analyzed: "
    f"{len(codebase)}"
)

print(
    f"Code elements documented: "
    f"{metrics['documented_elements']}"
)

print(
    f"Documentation completeness: "
    f"{metrics['documentation_completeness']:.2f}%"
)

print(
    f"Average semantic similarity: "
    f"{average_similarity:.4f}"
)

print(
    f"\nDocumentation file:"
    f"\n{OUTPUT_FILE}"
)


print("\n========================================")
print("        PIPELINE COMPLETED")
print("========================================")