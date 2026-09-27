import ast


def analyze_python_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    result = {
        "file": file_path,
        "source_code": source_code,
        "functions": [],
        "classes": [],
        "imports": []
    }


    # --------------------------------
    # Process top-level statements
    # --------------------------------

    for node in tree.body:

        # ----------------------------
        # Top-level function
        # ----------------------------

        if isinstance(node, ast.FunctionDef):

            function_code = ast.get_source_segment(
                source_code,
                node
            )

            result["functions"].append({
                "name": node.name,
                "parameters": [
                    arg.arg
                    for arg in node.args.args
                ],
                "line": node.lineno,
                "code": function_code
            })


        # ----------------------------
        # Class
        # ----------------------------

        elif isinstance(node, ast.ClassDef):

            class_info = {
                "name": node.name,
                "line": node.lineno,
                "methods": []
            }


            for child in node.body:

                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):

                    method_code = ast.get_source_segment(
                        source_code,
                        child
                    )

                    class_info["methods"].append({
                        "name": child.name,
                        "parameters": [
                            arg.arg
                            for arg in child.args.args
                        ],
                        "line": child.lineno,
                        "code": method_code
                    })


            result["classes"].append(
                class_info
            )


        # ----------------------------
        # Imports
        # ----------------------------

        elif isinstance(node, ast.Import):

            for alias in node.names:

                result["imports"].append(
                    alias.name
                )


        elif isinstance(node, ast.ImportFrom):

            if node.module:

                result["imports"].append(
                    node.module
                )


    return result