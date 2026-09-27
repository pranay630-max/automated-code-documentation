import ast
import os
import networkx as nx


def analyze_dependencies(folder):
    """
    Analyze Python file dependencies based on import statements.
    """

    graph = nx.DiGraph()

    # Find Python files
    for root, directories, files in os.walk(folder):

        for file in files:

            if not file.endswith(".py"):
                continue

            file_path = os.path.join(
                root,
                file
            )

            graph.add_node(file_path)

            # Read source code
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as source_file:

                source_code = source_file.read()

            # Parse source code
            tree = ast.parse(
                source_code
            )

            # Analyze imports
            for node in ast.walk(tree):

                imported_module = None

                if isinstance(
                    node,
                    ast.Import
                ):

                    for alias in node.names:

                        imported_module = (
                            alias.name
                        )

                        _add_dependency(
                            graph,
                            file_path,
                            imported_module,
                            folder
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom
                ):

                    if node.module:

                        imported_module = (
                            node.module
                        )

                        _add_dependency(
                            graph,
                            file_path,
                            imported_module,
                            folder
                        )

    return graph


def _add_dependency(
    graph,
    source_file,
    imported_module,
    folder
):
    """
    Add a dependency edge if the imported
    module belongs to the project.
    """

    module_name = imported_module.split(".")[0]

    for root, directories, files in os.walk(folder):

        for file in files:

            if file == module_name + ".py":

                target_file = os.path.join(
                    root,
                    file
                )

                graph.add_edge(
                    source_file,
                    target_file
                )