from llm.semantic_analyzer import tokenizer, model
import torch


def generate_project_summary(
    codebase,
    dependency_graph
):
    """
    Generate a high-level summary of the
    analyzed legacy codebase.
    """

    project_information = []

    for file_data in codebase:

        file_name = file_data["file"]

        project_information.append(
            f"\nFile: {file_name}"
        )

        if file_data["functions"]:

            project_information.append(
                "Functions:"
            )

            for function in file_data["functions"]:

                project_information.append(
                    f"- {function['name']}("
                    f"{', '.join(function['parameters'])})"
                )

        if file_data["classes"]:

            project_information.append(
                "Classes:"
            )

            for class_info in file_data["classes"]:

                project_information.append(
                    f"- {class_info['name']}"
                )

                for method in class_info["methods"]:

                    project_information.append(
                        f"  - {method['name']}("
                        f"{', '.join(method['parameters'])})"
                    )

        if file_data["imports"]:

            project_information.append(
                "Imports:"
            )

            for import_name in file_data["imports"]:

                project_information.append(
                    f"- {import_name}"
                )

    dependencies = []

    for source, target in dependency_graph.edges:

        dependencies.append(
            f"{source} -> {target}"
        )

    if dependencies:

        dependency_information = "\n".join(
            dependencies
        )

    else:

        dependency_information = (
            "No internal dependencies found."
        )

    project_data = "\n".join(
        project_information
    )

    prompt = f"""
You are an expert software architect.

Analyze the following structural information
extracted from a legacy Python codebase.

IMPORTANT RULES:

1. Base the summary only on the supplied information.
2. Do not invent functionality.
3. Do not assume business requirements that are not shown.
4. Do not claim that files depend on each other unless
   the dependency information explicitly shows it.
5. Clearly distinguish observed structure from interpretation.
6. Keep the summary concise and technically accurate.

Provide exactly these sections:

# Project Overview

Give a short description of what can be determined
from the codebase structure.

# Files and Components

Describe the important files, functions, classes,
and methods.

# Dependencies

Describe the internal file dependencies.

# Architecture Summary

Explain how the identified components are organized
and how they relate to each other.

# Key Observations

List important observations about the codebase
structure.

Codebase information:

{project_data}

Internal dependency information:

{dependency_information}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=600,
            temperature=0.1,
            do_sample=True
        )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response