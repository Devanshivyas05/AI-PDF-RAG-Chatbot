from langchain_core.documents import Document


def _normalize_score(score, min_score=0.0, max_score=1.0):
    if max_score <= min_score:
        return 0.0
    return max(0.0, min(1.0, (score - min_score) / (max_score - min_score)))


def retrieve_chunks(
    vector_db,
    bm25,
    documents,
    query,
    selected_pdf,
    k=5
):
    """
    Hybrid Retrieval

    1. Semantic Search
    2. BM25 Search
    3. Restore Full Metadata
    4. Merge Results
    5. Prioritize Figures for image queries
    """

    print(f"\n📂 Searching only in: {selected_pdf}")
    print("\n🔍 Performing Hybrid Search...\n")

    # ==================================================
    # Semantic Search
    # ==================================================

    semantic_results = vector_db.similarity_search_with_score(query, k=20)

    restored_semantic = []

    for result, score in semantic_results:

        source = result.metadata["source"]
        page = result.metadata["page"]
        chunk = result.metadata["chunk"]

        for doc in documents:

            if (
                doc.metadata["source"] == source
                and doc.metadata["page"] == page
                and doc.metadata["chunk"] == chunk
            ):
                doc.metadata["semantic_score"] = float(score)
                doc.metadata["retrieval_score"] = float(score)
                restored_semantic.append(doc)
                break

    semantic_results = [
        doc
        for doc in restored_semantic
        if doc.metadata["source"] == selected_pdf
    ]

    print(f"✅ Semantic Search Retrieved : {len(semantic_results)} chunks")

    # ==================================================
    # BM25
    # ==================================================

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    keyword_results = []

    for idx in ranked_indices:

        doc = documents[idx]

        if doc.metadata["source"] == selected_pdf:
            bm25_score = float(scores[idx])
            doc.metadata["bm25_score"] = bm25_score
            doc.metadata["retrieval_score"] = max(
                doc.metadata.get("retrieval_score", 0.0),
                bm25_score,
            )
            keyword_results.append(doc)

    print(f"✅ BM25 Search Retrieved      : {len(keyword_results)} chunks")

    # ==================================================
    # Merge
    # ==================================================

    merged = []
    seen = set()

    for doc in semantic_results + keyword_results:

        key = (
            doc.metadata["source"],
            doc.metadata["page"],
            doc.metadata["chunk"]
        )

        if key not in seen:
            merged.append(doc)
            seen.add(key)

    # ==================================================
    # PRIORITIZE MEDIA AND TABLE DOCS FOR MATCHING QUERIES
    # ==================================================

    query_lower = query.lower()

    image_keywords = [
        "image",
        "figure",
        "diagram",
        "graph",
        "flowchart",
        "chart",
        "display",
        "picture",
        "architecture",
        "cnn",
        "ann",
        "decision tree",
        "tree"
    ]

    table_keywords = [
        "table",
        "tabular",
        "rows",
        "columns",
        "matrix",
        "confusion",
        "accuracy"
    ]

    is_image_query = any(word in query_lower for word in image_keywords)
    is_table_query = any(word in query_lower for word in table_keywords)

    def score_doc(doc):
        metadata = doc.metadata
        score = 0
        doc_type = metadata.get("type")

        if is_table_query and doc_type == "table":
            score += 100
        if is_image_query and doc_type in {"figure", "image"}:
            score += 100

        if doc_type == "table":
            score += 20
        if doc_type in {"figure", "image"}:
            score += 15

        query_terms = [term for term in query_lower.split() if len(term) > 2]
        content = (doc.page_content + " " + str(metadata.get("ocr_text", "")) + " " + str(metadata.get("page_context", ""))).lower()

        for term in query_terms:
            if term in content:
                score += 5

        return score

    if merged:
        ranked = sorted(merged, key=score_doc, reverse=True)
        merged = ranked

    if merged:
        page_deduped = []
        seen_pages = set()
        for doc in merged:
            page_key = (doc.metadata.get("source"), doc.metadata.get("page"))
            if page_key in seen_pages:
                continue
            seen_pages.add(page_key)
            page_deduped.append(doc)
        merged = page_deduped

    if is_image_query and merged:
        media_docs = [d for d in merged if d.metadata.get("type") in {"figure", "image"}]
        if media_docs:
            print("\n🖼 Prioritizing image/figure documents...")
            merged = media_docs + [d for d in merged if d.metadata.get("type") not in {"figure", "image"}]

    if is_table_query and merged:
        table_docs = [d for d in merged if d.metadata.get("type") == "table"]
        if table_docs:
            print("\n📊 Prioritizing table documents...")
            merged = table_docs + [d for d in merged if d.metadata.get("type") != "table"]

    print(f"\n📚 Total Unique Chunks : {len(merged)}")

    print("\n========== RETRIEVED ==========")

    top_docs = merged[:k]

    for i, doc in enumerate(top_docs, start=1):

        print(
            f"{i}.",
            doc.metadata.get("type"),
            "| Page",
            doc.metadata.get("page"),
        )

        print(f"Score : {doc.metadata.get('retrieval_score', 0.0):.4f}")
        print(doc.page_content[:120])
        print("-" * 50)

    return top_docs