import re


def evaluate_completeness(codebase, documented_items):
    """
    Calculate documentation completeness.

    Completeness =
    documented code elements / total code elements * 100
    """

    total_elements = 0

    for file_data in codebase:

        # Count top-level functions
        total_elements += len(
            file_data["functions"]
        )

        # Count class methods
        for class_info in file_data["classes"]:

            total_elements += len(
                class_info["methods"]
            )

    documented_elements = len(
        documented_items
    )

    if total_elements == 0:
        return 0

    completeness = (
        documented_elements
        / total_elements
    ) * 100

    return completeness


def check_documentation_presence(
    documented_items
):
    """
    Check whether each documented item
    contains generated documentation.
    """

    documented_count = 0

    for item in documented_items:

        documentation = item.get(
            "documentation",
            ""
        )

        if documentation.strip():

            documented_count += 1

    return documented_count


def calculate_basic_metrics(
    codebase,
    documented_items
):

    total_elements = 0

    for file_data in codebase:

        total_elements += len(
            file_data["functions"]
        )

        for class_info in file_data["classes"]:

            total_elements += len(
                class_info["methods"]
            )

    documented_elements = check_documentation_presence(
        documented_items
    )

    if total_elements == 0:

        completeness = 0

    else:

        completeness = (
            documented_elements
            / total_elements
        ) * 100

    return {
        "total_code_elements": total_elements,
        "documented_elements": documented_elements,
        "documentation_completeness": completeness
    }