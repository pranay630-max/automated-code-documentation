from analyzer.dependency_analyzer import analyze_dependencies


CODEBASE_FOLDER = "input/legacy_project"


graph = analyze_dependencies(
    CODEBASE_FOLDER
)


print("\n================================")
print("       DEPENDENCY ANALYSIS")
print("================================")

print(
    f"\nTotal files: {graph.number_of_nodes()}"
)

print(
    f"Total dependencies: "
    f"{graph.number_of_edges()}"
)


print("\nFiles:")

for node in graph.nodes:

    print(
        f"  - {node}"
    )


print("\nDependencies:")

if graph.number_of_edges() == 0:

    print(
        "  No internal dependencies found."
    )

else:

    for source, target in graph.edges:

        print(
            f"  {source} -> {target}"
        )