import ast
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


# =========================================================
# MODEL CONFIGURATION
# =========================================================

# =========================================================
# MODEL CONFIGURATION
# =========================================================

# Use the smaller model for deployment compatibility.
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

print("Loading model...")
print(f"Model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# Use GPU when available, otherwise CPU.
if torch.cuda.is_available():
    print("GPU detected. Loading model on GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16,
        device_map="auto"
    )
else:
    print("No GPU detected. Loading model on CPU...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32
    )

model.eval()

print("Model loaded successfully.")


# =========================================================
# EXTRACT FACTS FROM SOURCE CODE
# =========================================================

def extract_source_facts(function_code):

    tree = ast.parse(function_code)

    function_node = None

    for node in tree.body:

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):
            function_node = node
            break

    if function_node is None:
        return "No function definition found."

    facts = []

    # -----------------------------------------------------
    # Function name
    # -----------------------------------------------------

    facts.append(
        f"Function name: {function_node.name}"
    )

    # -----------------------------------------------------
    # Parameters
    # -----------------------------------------------------

    parameters = [
        arg.arg
        for arg in function_node.args.args
    ]

    user_parameters = [
        parameter
        for parameter in parameters
        if parameter not in ["self", "cls"]
    ]

    facts.append(
        f"Exact parameters: {parameters}"
    )

    facts.append(
        f"User-provided parameters: {user_parameters}"
    )

    # -----------------------------------------------------
    # Return statements
    # -----------------------------------------------------

    return_nodes = [
        node
        for node in ast.walk(function_node)
        if isinstance(node, ast.Return)
    ]

    if return_nodes:

        return_values = []

        for node in return_nodes:

            if node.value is None:

                return_values.append(
                    "None"
                )

            else:

                return_values.append(
                    ast.unparse(node.value)
                )

        facts.append(
            "Explicit return expressions: "
            + ", ".join(return_values)
        )

    else:

        facts.append(
            "No explicit return statement exists."
        )

    # -----------------------------------------------------
    # If conditions
    # -----------------------------------------------------

    if_nodes = [
        node
        for node in ast.walk(function_node)
        if isinstance(node, ast.If)
    ]

    if if_nodes:

        for node in if_nodes:

            facts.append(
                "Explicit condition: "
                + ast.unparse(node.test)
            )

    else:

        facts.append(
            "No if/elif condition exists."
        )

    # -----------------------------------------------------
    # Loops
    # -----------------------------------------------------

    loop_nodes = [
        node
        for node in ast.walk(function_node)
        if isinstance(
            node,
            (
                ast.For,
                ast.While
            )
        )
    ]

    if loop_nodes:

        for node in loop_nodes:

            facts.append(
                "Explicit loop: "
                + ast.unparse(node)
            )

    else:

        facts.append(
            "No loop exists."
        )

    # -----------------------------------------------------
    # Explicit exceptions
    # -----------------------------------------------------

    raise_nodes = [
        node
        for node in ast.walk(function_node)
        if isinstance(node, ast.Raise)
    ]

    if raise_nodes:

        for node in raise_nodes:

            facts.append(
                "Explicit exception raised: "
                + ast.unparse(node)
            )

    else:

        facts.append(
            "No explicit exception is raised."
        )

    # -----------------------------------------------------
    # Exception handlers
    # -----------------------------------------------------

    except_nodes = [
        node
        for node in ast.walk(function_node)
        if isinstance(node, ast.ExceptHandler)
    ]

    if except_nodes:

        for node in except_nodes:

            if node.type:

                facts.append(
                    "Explicit exception handled: "
                    + ast.unparse(node.type)
                )

    else:

        facts.append(
            "No exception is explicitly handled."
        )

    # -----------------------------------------------------
    # Attribute accesses
    # -----------------------------------------------------

    attributes = []

    for node in ast.walk(function_node):

        if isinstance(node, ast.Attribute):

            expression = ast.unparse(node)

            if expression not in attributes:

                attributes.append(expression)

    if attributes:

        facts.append(
            "Attribute accesses: "
            + ", ".join(attributes)
        )

    # -----------------------------------------------------
    # Function calls
    # -----------------------------------------------------

    calls = []

    for node in ast.walk(function_node):

        if isinstance(node, ast.Call):

            expression = ast.unparse(node.func)

            if expression not in calls:

                calls.append(expression)

    if calls:

        facts.append(
            "Function/method calls: "
            + ", ".join(calls)
        )

    return "\n".join(
        f"- {fact}"
        for fact in facts
    )


# =========================================================
# DOCUMENTATION SANITIZER
# =========================================================

def sanitize_documentation(
    documentation,
    function_code
):

    """
    Remove unsupported claims generated by the LLM.

    The source code remains the authority.
    """

    tree = ast.parse(function_code)

    function_node = None

    for node in tree.body:

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            function_node = node
            break

    if function_node is None:
        return documentation

    parameters = [
        arg.arg
        for arg in function_node.args.args
        if arg.arg not in ["self", "cls"]
    ]

    # -----------------------------------------------------
    # REMOVE UNSUPPORTED PARAMETER LINES
    # -----------------------------------------------------

    lines = documentation.splitlines()

    cleaned_lines = []

    inside_parameters = False

    for line in lines:

        if line.strip() == "### Parameters":

            inside_parameters = True

            cleaned_lines.append(line)

            continue

        if inside_parameters and line.startswith("### "):

            inside_parameters = False

        if inside_parameters:

            stripped = line.strip()

            if stripped.startswith("-"):

                parameter_name = stripped[1:].strip()

                if "`" in parameter_name:

                    parts = parameter_name.split("`")

                    if len(parts) >= 2:

                        parameter_name = parts[1]

                parameter_name = (
                    parameter_name
                    .split(":")[0]
                    .strip()
                )

                parameter_name = (
                    parameter_name
                    .split("(")[0]
                    .strip()
                )

                if parameter_name in ["self", "cls"]:

                    continue

                if (
                    parameter_name
                    and parameter_name not in parameters
                ):

                    continue

        cleaned_lines.append(line)

    documentation = "\n".join(
        cleaned_lines
    )

    # -----------------------------------------------------
    # REMOVE UNSUPPORTED EXCEPTION CLAIMS
    # -----------------------------------------------------

    explicit_exceptions = set()

    for node in ast.walk(function_node):

        if isinstance(node, ast.Raise):

            if node.exc:

                if isinstance(
                    node.exc,
                    ast.Call
                ):

                    if isinstance(
                        node.exc.func,
                        ast.Name
                    ):

                        explicit_exceptions.add(
                            node.exc.func.id
                        )

                elif isinstance(
                    node.exc,
                    ast.Name
                ):

                    explicit_exceptions.add(
                        node.exc.id
                    )

        elif isinstance(
            node,
            ast.ExceptHandler
        ):

            if node.type:

                if isinstance(
                    node.type,
                    ast.Name
                ):

                    explicit_exceptions.add(
                        node.type.id
                    )

    exception_names = [
        "ValueError",
        "TypeError",
        "KeyError",
        "IndexError",
        "AttributeError",
        "ZeroDivisionError"
    ]

    for exception_name in exception_names:

        if exception_name not in explicit_exceptions:

            documentation = documentation.replace(
                exception_name,
                ""
            )

    # -----------------------------------------------------
    # REMOVE UNSUPPORTED REQUIREMENT PHRASES
    # -----------------------------------------------------

    unsupported_phrases = [

        "must be a non-empty string",

        "must be a positive integer",

        "must be a positive float",

        "must be positive",

        "must be negative",

        "must be non-empty",

        "requires a valid",

        "requires valid",

        "expects a valid",

        "must be valid",

        "invalid input",

        "raises ValueError",

        "will raise ValueError",

        "raises TypeError",

        "will raise TypeError",

        "must be a string",

        "must be a number",

        "must be numeric",

        "must be a positive number",

        "will cause an error",

        "an error will occur"
    ]

    for phrase in unsupported_phrases:

        documentation = documentation.replace(
            phrase,
            ""
        )

    # -----------------------------------------------------
    # REMOVE UNSUPPORTED CONDITIONS AND EDGE CASES
    # -----------------------------------------------------

    has_explicit_conditions = any(
        isinstance(
            node,
            ast.If
        )
        for node in ast.walk(
            function_node
        )
    )

    if not has_explicit_conditions:

        lines = documentation.splitlines()

        cleaned_lines = []

        skip_section = False

        for line in lines:

            if (
                line.strip()
                == "### Important Conditions"
            ):

                skip_section = True

                cleaned_lines.append(line)

                cleaned_lines.append(
                    "No specific conditions are "
                    "explicitly handled by the code."
                )

                continue

            if (
                line.strip()
                == "### Possible Edge Cases"
            ):

                skip_section = True

                cleaned_lines.append(line)

                cleaned_lines.append(
                    "No specific edge case is "
                    "explicitly handled by the code."
                )

                continue

            if (
                skip_section
                and line.startswith("### ")
            ):

                skip_section = False

            if not skip_section:

                cleaned_lines.append(line)

        documentation = "\n".join(
            cleaned_lines
        )

    # -----------------------------------------------------
    # CONSTRUCTOR CORRECTION
    # -----------------------------------------------------

    if function_node.name == "__init__":

        documentation = documentation.replace(
            "### Return Value\n- None",
            "### Return Value\n"
            "- No value is explicitly returned "
            "by the code."
        )

        documentation = documentation.replace(
            "No specific return value is "
            "explicitly handled by the code.",
            "No value is explicitly returned "
            "by the code."
        )

    # -----------------------------------------------------
    # CLEAN EMPTY LINES
    # -----------------------------------------------------

    cleaned_lines = []

    for line in documentation.splitlines():

        if line.strip() == "":

            if (
                cleaned_lines
                and cleaned_lines[-1].strip() == ""
            ):

                continue

        cleaned_lines.append(line)

    return "\n".join(
        cleaned_lines
    ).strip()


# =========================================================
# GENERATE DOCUMENTATION
# =========================================================

def generate_documentation(
    function_code
):

    source_facts = extract_source_facts(
        function_code
    )

    prompt = f"""
You are a strict Python code documentation generator.

Document the supplied Python function.

The source code and AST facts are the ONLY authority.

Do not invent behavior.

=========================================================
SOURCE FACTS
=========================================================

{source_facts}

=========================================================
STRICT RULES
=========================================================

1. Use the exact function signature.

2. Document ONLY parameters listed as
   "User-provided parameters".

3. Never document self or cls as parameters.

4. Never convert self.attribute into a parameter.

5. Never invent parameter types.

6. Never invent input requirements.

7. Never say a parameter must be positive,
   negative, non-empty, valid, or a specific type
   unless the source explicitly checks it.

8. Never invent exceptions.

9. Never mention hypothetical Python runtime errors.

10. Only describe explicit conditions from the source.

11. Only describe explicit loops from the source.

12. Only describe explicit return behavior.

13. If there are no explicit edge-case checks,
write exactly:

No specific edge case is explicitly handled by the code.

14. Do not use words such as:
assuming, requires, expects, must be,
unless directly supported by the source.

15. Keep the documentation concise.

16. Do not describe possible runtime errors.

17. Do not infer types from variable names.

18. Do not infer class types for self.

19. Do not invent behavior that is not
observable in the source code.

=========================================================
REQUIRED FORMAT
=========================================================

### Function Purpose

### Parameters

### Return Value

### Step-by-Step Algorithm

### Important Conditions

### Possible Edge Cases

### Example Usage

=========================================================
PARAMETER RULE
=========================================================

If there are no user-provided parameters, write:

No user-provided parameters.

Do not document self or cls.

=========================================================
CONSTRUCTOR RULE
=========================================================

If the function is __init__ and there is no
explicit return statement, write:

No value is explicitly returned by the code.

Do not invent exceptions.

=========================================================
SOURCE CODE
=========================================================

{function_code}
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
        return_tensors="pt",
        truncation=True,
        max_length=3072
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.inference_mode():

        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False,
            repetition_penalty=1.05,
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    # -----------------------------------------------------
    # FINAL DETERMINISTIC CLEANUP
    # -----------------------------------------------------

    response = sanitize_documentation(
        response,
        function_code
    )

    return response