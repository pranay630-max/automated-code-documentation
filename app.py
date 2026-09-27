
import streamlit as st

from analyzer.codebase_analyzer import analyze_codebase
from analyzer.dependency_analyzer import analyze_dependencies
from evaluation.documentation_evaluator import calculate_basic_metrics
from evaluation.documentation_validator import validate_documentation


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Code Documentation System",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 Automated Code Documentation System")

st.write(
    "An LLM-driven system for analyzing legacy Python code "
    "and automatically generating and validating documentation."
)

st.divider()


# =========================================================
# PROJECT PATH
# =========================================================

CODEBASE_FOLDER = "input/legacy_project"


# =========================================================
# CACHED CODEBASE ANALYSIS
# =========================================================

@st.cache_data(show_spinner="Analyzing Python files...")
def cached_codebase_analysis(folder):
    return analyze_codebase(folder)


# =========================================================
# CACHED DEPENDENCY ANALYSIS
# =========================================================

@st.cache_resource(show_spinner="Analyzing dependencies...")
def cached_dependency_analysis(folder):
    return analyze_dependencies(folder)


# =========================================================
# CACHED DOCUMENTATION GENERATION
# =========================================================

@st.cache_data(show_spinner="Generating AI documentation...")
def cached_documentation_generation(codebase):
    from llm.semantic_analyzer import generate_documentation
    documented_items = []

    # -----------------------------------------------------
    # Functions
    # -----------------------------------------------------

    for file_data in codebase:

        file_path = file_data["file"]

        for function in file_data["functions"]:

            documentation = generate_documentation(
                function["code"]
            )

            documented_items.append({
                "name": function["name"],
                "type": "function",
                "file": file_path,
                "code": function["code"],
                "documentation": documentation,
                "parameters": function["parameters"]
            })

    # -----------------------------------------------------
    # Class methods
    # -----------------------------------------------------

    for file_data in codebase:

        file_path = file_data["file"]

        for class_info in file_data["classes"]:

            for method in class_info["methods"]:

                documentation = generate_documentation(
                    method["code"]
                )

                documented_items.append({
                    "name": method["name"],
                    "type": "method",
                    "class": class_info["name"],
                    "file": file_path,
                    "code": method["code"],
                    "documentation": documentation,
                    "parameters": method["parameters"]
                })

    return documented_items


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False

if "documentation_done" not in st.session_state:
    st.session_state["documentation_done"] = False


# =========================================================
# ANALYZE CODEBASE BUTTON
# =========================================================

print("DEBUG: Reached Analyze Codebase section")

if st.button(
    "🔍 Analyze Codebase",
    use_container_width=True
):

    print("DEBUG: BUTTON CLICKED")

    # -----------------------------------------------------
    # CODEBASE ANALYSIS
    # -----------------------------------------------------

    try:

        with st.spinner(
            "Analyzing codebase..."
        ):

            codebase = cached_codebase_analysis(
                CODEBASE_FOLDER
            )

        st.session_state["codebase"] = codebase

        st.success(
            "✅ Codebase analysis completed successfully."
        )

    except Exception as error:

        st.error(
            "❌ Codebase analysis failed."
        )

        st.exception(error)

        st.stop()


    # -----------------------------------------------------
    # DEPENDENCY ANALYSIS
    # -----------------------------------------------------

    try:

        with st.spinner(
            "Analyzing dependencies..."
        ):

            dependency_graph = cached_dependency_analysis(
                CODEBASE_FOLDER
            )

        st.session_state[
            "dependency_graph"
        ] = dependency_graph

    except Exception as error:

        st.error(
            "❌ Dependency analysis failed."
        )

        st.exception(error)

        st.stop()


    # -----------------------------------------------------
    # UPDATE SESSION STATE
    # -----------------------------------------------------

    st.session_state[
        "analysis_done"
    ] = True

    st.session_state[
        "documentation_done"
    ] = False

    st.success(
        "🎉 Complete codebase analysis finished successfully."
    )


# =========================================================
# DISPLAY ANALYSIS
# =========================================================

if st.session_state.get(
    "analysis_done",
    False
):

    codebase = st.session_state[
        "codebase"
    ]

    dependency_graph = st.session_state[
        "dependency_graph"
    ]


    # =====================================================
    # CODEBASE METRICS
    # =====================================================

    total_files = len(codebase)

    total_functions = 0

    total_classes = 0

    total_methods = 0

    for file_data in codebase:

        total_functions += len(
            file_data["functions"]
        )

        total_classes += len(
            file_data["classes"]
        )

        for class_info in file_data["classes"]:

            total_methods += len(
                class_info["methods"]
            )


    total_elements = (
        total_functions +
        total_methods
    )

    total_dependencies = (
        dependency_graph.number_of_edges()
    )


    # =====================================================
    # CODEBASE OVERVIEW
    # =====================================================

    st.subheader(
        "📊 Codebase Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Python Files",
            total_files
        )

    with col2:

        st.metric(
            "Functions",
            total_functions
        )

    with col3:

        st.metric(
            "Classes",
            total_classes
        )

    with col4:

        st.metric(
            "Dependencies",
            total_dependencies
        )


    st.divider()


    # =====================================================
    # FILE ANALYSIS
    # =====================================================

    st.subheader(
        "📁 Files Analyzed"
    )

    for file_data in codebase:

        with st.expander(
            f"📄 {file_data['file']}"
        ):

            if file_data["functions"]:

                st.markdown(
                    "### Functions"
                )

                for function in file_data["functions"]:

                    st.write(
                        f"• `{function['name']}()`"
                    )


            if file_data["classes"]:

                st.markdown(
                    "### Classes"
                )

                for class_info in file_data["classes"]:

                    st.write(
                        f"• `{class_info['name']}`"
                    )

                    for method in class_info["methods"]:

                        st.write(
                            f"   └── `{method['name']}()`"
                        )


    # =====================================================
    # DEPENDENCY ANALYSIS
    # =====================================================

    st.divider()

    st.subheader(
        "🔗 Dependency Analysis"
    )

    if total_dependencies == 0:

        st.info(
            "No internal dependencies were detected."
        )

    else:

        for source, target in dependency_graph.edges():

            st.write(
                f"`{source}` → `{target}`"
            )


    # =====================================================
    # DOCUMENTATION GENERATION
    # =====================================================

    st.divider()

    st.subheader(
        "🤖 AI Documentation Generation"
    )

    if st.button(
        "🚀 Generate Documentation",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Generating AI documentation..."
            ):

                documented_items = (
                    cached_documentation_generation(
                        codebase
                    )
                )

            st.session_state[
                "documented_items"
            ] = documented_items

            st.session_state[
                "documentation_done"
            ] = True

            st.success(
                "✅ AI documentation generated successfully!"
            )

        except Exception as error:

            st.error(
                "❌ Documentation generation failed."
            )

            st.exception(error)


# =========================================================
# DOCUMENTATION RESULTS
# =========================================================

if st.session_state.get(
    "documentation_done",
    False
):

    documented_items = st.session_state[
        "documented_items"
    ]

    codebase = st.session_state[
        "codebase"
    ]


    # =====================================================
    # DOCUMENTATION METRICS
    # =====================================================

    st.divider()

    st.subheader(
        "📚 Generated Documentation"
    )

    metrics = calculate_basic_metrics(
        codebase,
        documented_items
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Code Elements",
            metrics[
                "total_code_elements"
            ]
        )

    with col2:

        st.metric(
            "Documentation Completeness",
            f"{metrics['documentation_completeness']:.2f}%"
        )


    # =====================================================
    # VALIDATION
    # =====================================================

    st.divider()

    st.subheader(
        "🔍 Documentation Validation"
    )

    validation_results = []

    for item in documented_items:

        if item["type"] == "method":

            display_name = (
                f"{item['class']}."
                f"{item['name']}()"
            )

        else:

            display_name = (
                f"{item['name']}()"
            )


        validation_result = (
            validate_documentation(

                item["code"],

                item["documentation"],

                item["parameters"]

            )
        )


        validation_results.append({

            "name": display_name,

            "result": validation_result

        })


        if validation_result["status"] == (
            "No Issues Detected"
        ):

            status_text = "✅ Verified"

        else:

            status_text = "⚠️ Needs Review"


        with st.expander(
            f"{status_text} | {display_name}"
        ):

            st.markdown(
                f"**Source File:** "
                f"`{item['file']}`"
            )

            st.markdown(
                f"**Validation Status:** "
                f"{validation_result['status']}"
            )


            if validation_result["issues"]:

                st.markdown(
                    "### ⚠️ Detected Issues"
                )

                for issue in (
                    validation_result["issues"]
                ):

                    st.warning(issue)

            else:

                st.success(
                    "No unsupported claims detected."
                )


            st.markdown(
                "### 📝 Generated Documentation"
            )

            st.markdown(
                item["documentation"]
            )


            st.markdown(
                "### 💻 Source Code"
            )

            st.code(
                item["code"],
                language="python"
            )


    # =====================================================
    # VALIDATION SUMMARY
    # =====================================================

    st.divider()

    st.subheader(
        "📈 Validation Summary"
    )

    verified_count = 0

    review_count = 0

    for validation_item in validation_results:

        result = validation_item["result"]

        if result["status"] == (
            "No Issues Detected"
        ):

            verified_count += 1

        else:

            review_count += 1


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Elements",
            len(documented_items)
        )

    with col2:

        st.metric(
            "Verified",
            verified_count
        )

    with col3:

        st.metric(
            "Needs Review",
            review_count
        )


    st.caption(
        "The validator checks whether generated "
        "documentation contains claims that can "
        "be supported by the source code."
    )

