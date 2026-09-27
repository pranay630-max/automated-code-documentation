from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


print("Loading semantic evaluation model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Semantic evaluation model loaded.")


def calculate_semantic_similarity(
    source_code,
    documentation
):
    """
    Calculate semantic similarity between
    source code and generated documentation.
    """

    source_embedding = model.encode(
        [source_code]
    )

    documentation_embedding = model.encode(
        [documentation]
    )

    similarity = cosine_similarity(
        source_embedding,
        documentation_embedding
    )[0][0]

    return float(similarity)


def evaluate_documentation_semantics(
    documented_items
):
    """
    Calculate semantic similarity for
    every documented code element.
    """

    results = []

    for item in documented_items:

        source_code = item.get(
            "code",
            ""
        )

        documentation = item.get(
            "documentation",
            ""
        )

        if not source_code or not documentation:
            continue

        similarity = calculate_semantic_similarity(
            source_code,
            documentation
        )

        results.append({
            "name": item["name"],
            "similarity": similarity
        })

    return results