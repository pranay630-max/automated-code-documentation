from analyzer.codebase_analyzer import analyze_codebase
from analyzer.dependency_analyzer import analyze_dependencies

from llm.project_summary import (
    generate_project_summary
)


CODEBASE_FOLDER = "input/legacy_project"


print("\n========================================")
print("       PROJECT SUMMARY GENERATION")
print("========================================")


# Analyze codebase
codebase = analyze_codebase(
    CODEBASE_FOLDER
)


# Analyze dependencies
dependency_graph = analyze_dependencies(
    CODEBASE_FOLDER
)


print("\nGenerating project summary...")


# Generate summary
summary = generate_project_summary(
    codebase,
    dependency_graph
)


print("\n========================================")
print("           PROJECT SUMMARY")
print("========================================")

print(summary)

print("\n========================================")
print("       SUMMARY GENERATION COMPLETE")
print("========================================")