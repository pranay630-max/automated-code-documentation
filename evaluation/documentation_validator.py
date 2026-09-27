
import re


def validate_documentation(
    source_code,
    documentation,
    parameters
):
    """
    Validate generated documentation against
    observable facts in the source code.

    The validator checks:
    1. Missing parameters
    2. Extra/incorrect parameters
    3. Unsupported type claims
    4. Unsupported exception claims
    5. Unsupported validation requirements
    """

    issues = []

    # =====================================================
    # 1. PARAMETER VALIDATION
    # =====================================================

    # Remove implementation parameters.
    user_parameters = [
        parameter
        for parameter in parameters
        if parameter not in ["self", "cls"]
    ]

    parameter_section = re.search(
        r"### Parameters(.*?)(?="
        r"### Return Value|"
        r"### Step-by-Step Algorithm|"
        r"### Important Conditions|"
        r"### Possible Edge Cases|"
        r"### Example Usage|"
        r"$)",
        documentation,
        re.DOTALL
    )

    if parameter_section:

        parameter_text = parameter_section.group(1)

        # -------------------------------------------------
        # Check for missing parameters
        # -------------------------------------------------

        for parameter in user_parameters:

            if not re.search(
                rf"\b{re.escape(parameter)}\b",
                parameter_text
            ):

                issues.append(
                    f"Parameter '{parameter}' "
                    f"is missing from the documentation."
                )

        # -------------------------------------------------
        # Check for extra/incorrect parameters
        # -------------------------------------------------

        documented_parameters = re.findall(
            r"^\s*[-*]?\s*`?([A-Za-z_][A-Za-z0-9_]*)`?\s*:",
            parameter_text,
            re.MULTILINE
        )

        documented_parameters = [
            parameter
            for parameter in documented_parameters
            if parameter not in ["self", "cls"]
        ]

        for parameter in documented_parameters:

            if parameter not in user_parameters:

                issues.append(
                    f"Parameter '{parameter}' is documented "
                    f"but is not present in the function signature."
                )

    # =====================================================
    # 2. TYPE CLAIM DETECTION
    # =====================================================

    type_patterns = [
        r"\btype is\b",
        r"\btyped as\b",
        r"\bmust be of type\b",
        r"\bhas type\b"
    ]

    has_type_annotations = bool(
        re.search(
            r"\b[A-Za-z_][A-Za-z0-9_]*\s*:\s*"
            r"[A-Za-z_][A-Za-z0-9_\[\], .]*",
            source_code
        )
    )

    if not has_type_annotations:

        for pattern in type_patterns:

            if re.search(
                pattern,
                documentation,
                re.IGNORECASE
            ):

                issues.append(
                    "Documentation makes an explicit "
                    "type claim that is not supported "
                    "by a source-code type annotation."
                )

                break

    # =====================================================
    # 3. UNSUPPORTED EXCEPTION CLAIMS
    # =====================================================

    exception_patterns = {
        "TypeError": r"\bTypeError\b",
        "ValueError": r"\bValueError\b",
        "KeyError": r"\bKeyError\b",
        "IndexError": r"\bIndexError\b",
        "ZeroDivisionError": r"\bZeroDivisionError\b",
        "AttributeError": r"\bAttributeError\b"
    }

    for exception_name, pattern in exception_patterns.items():

        if not re.search(
            pattern,
            documentation
        ):
            continue

        # -------------------------------------------------
        # Explicitly raised exception
        # -------------------------------------------------

        explicit_raise = re.search(
            rf"\braise\s+{re.escape(exception_name)}\b",
            source_code
        )

        if explicit_raise:
            continue

        # -------------------------------------------------
        # Explicitly caught exception
        # -------------------------------------------------

        explicit_catch = re.search(
            rf"\bexcept\s+{re.escape(exception_name)}\b",
            source_code
        )

        if explicit_catch:
            continue

        # -------------------------------------------------
        # Exception caused by an operation that is
        # directly observable in the source.
        #
        # We do NOT automatically treat every possible
        # Python exception as an actual documented behavior.
        # -------------------------------------------------

        observable_exception = False

        if exception_name == "ZeroDivisionError":

            if re.search(
                r"/\s*[A-Za-z_][A-Za-z0-9_]*",
                source_code
            ):
                observable_exception = True

        elif exception_name == "AttributeError":

            if re.search(
                r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*",
                source_code
            ):
                observable_exception = True

        elif exception_name == "TypeError":

            # Function calls/operators may potentially produce
            # TypeError, but do not treat this as a guaranteed
            # behavior.
            observable_exception = False

        elif exception_name == "ValueError":

            # No explicit source evidence means we should not
            # claim that ValueError actually occurs.
            observable_exception = False

        elif exception_name == "KeyError":

            if re.search(
                r"\[[^\]]+\]",
                source_code
            ):
                observable_exception = True

        elif exception_name == "IndexError":

            if re.search(
                r"\[[^\]]+\]",
                source_code
            ):
                observable_exception = True

        if not observable_exception:

            issues.append(
                f"Documentation mentions {exception_name}, "
                f"but the source code does not explicitly "
                f"raise or handle this exception."
            )

    # =====================================================
    # 4. UNSUPPORTED VALIDATION CLAIMS
    # =====================================================

    validation_patterns = [
        r"\binput validation is performed\b",
        r"\bvalidates the input\b",
        r"\bvalidates the parameter\b",
        r"\brejects invalid input\b",
        r"\bmust be non-empty\b",
        r"\bmust be positive\b",
        r"\bcannot be None\b"
    ]

    for pattern in validation_patterns:

        if re.search(
            pattern,
            documentation,
            re.IGNORECASE
        ):

            # Look for observable validation logic.
            has_condition = bool(
                re.search(
                    r"\b(if|elif)\b",
                    source_code
                )
            )

            if not has_condition:

                issues.append(
                    "Documentation contains a possible "
                    "validation claim that is not supported "
                    "by an observable condition in the source."
                )

                break

    # =====================================================
    # 5. UNSUPPORTED REQUIREMENT CLAIMS
    # =====================================================

    requirement_patterns = [
        r"\bmust be provided\b",
        r"\bmust be a\b",
        r"\bmust contain\b",
        r"\brequires a valid\b",
        r"\brequires valid\b",
        r"\bexpects a valid\b"
    ]

    for pattern in requirement_patterns:

        if re.search(
            pattern,
            documentation,
            re.IGNORECASE
        ):

            # Only accept strong requirement claims when
            # there is an observable condition supporting them.
            has_condition = bool(
                re.search(
                    r"\b(if|elif)\b",
                    source_code
                )
            )

            if not has_condition:

                issues.append(
                    "Documentation contains an unsupported "
                    "input requirement."
                )

                break

    # =====================================================
    # 6. FINAL RESULT
    # =====================================================

    if issues:

        status = "Needs Review"

    else:

        status = "No Issues Detected"

    return {
        "status": status,
        "issues": issues,
        "issue_count": len(issues)
    }
