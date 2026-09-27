from analyzer.codebase_analyzer import analyze_codebase
from llm.semantic_analyzer import generate_documentation
from evaluation.semantic_evaluator import (
    calculate_semantic_similarity
)


CODEBASE_FOLDER = "input/legacy_project"


print("\n========================================")
print("       SEMANTIC EVALUATION TEST")
print("========================================")


# Analyze codebase
codebase = analyze_codebase(
    CODEBASE_FOLDER
)


results = []


for file_data in codebase:

    # -----------------------------
    # Top-level functions
    # -----------------------------

    for function in file_data["functions"]:

        print(
            f"\nAnalyzing: {function['name']}"
        )

        documentation = generate_documentation(
            function["code"]
        )

        similarity = calculate_semantic_similarity(
            function["code"],
            documentation
        )

        results.append({
            "name": function["name"],
            "similarity": similarity
        })

        print(
            f"Semantic similarity: "
            f"{similarity:.4f}"
        )


    # -----------------------------
    # Class methods
    # -----------------------------

    for class_info in file_data["classes"]:

        for method in class_info["methods"]:

            print(
                f"\nAnalyzing: "
                f"{class_info['name']}.{method['name']}"
            )

            documentation = generate_documentation(
                method["code"]
            )

            similarity = calculate_semantic_similarity(
                method["code"],
                documentation
            )

            results.append({
                "name": method["name"],
                "similarity": similarity
            })

            print(
                f"Semantic similarity: "
                f"{similarity:.4f}"
            )


# -----------------------------
# Overall score
# -----------------------------

if results:

    average_similarity = (
        sum(
            item["similarity"]
            for item in results
        )
        / len(results)
    )

else:

    average_similarity = 0


print("\n========================================")
print("        SEMANTIC EVALUATION")
print("========================================")

for result in results:

    print(
        f"{result['name']}: "
        f"{result['similarity']:.4f}"
    )

print(
    f"\nAverage semantic similarity: "
    f"{average_similarity:.4f}"
)

print("========================================")