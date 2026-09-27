from pathlib import Path


def create_documentation(functions, output_file):
    """
    Create a Markdown documentation file from
    LLM-generated documentation.
    """

    documentation = []

    documentation.append("# Automated Code Documentation\n")

    documentation.append(
        "Generated automatically using "
        "AST analysis and an LLM.\n"
    )

    for function in functions:

        documentation.append(
            f"\n## Function: `{function['name']}`\n"
        )

        documentation.append(
            f"**Source file:** `{function['file']}`\n"
        )

        documentation.append(
            function["documentation"]
        )

        documentation.append("\n---\n")

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        "\n".join(documentation),
        encoding="utf-8"
    )

    print(
        f"\nDocumentation generated: "
        f"{output_path}"
    )