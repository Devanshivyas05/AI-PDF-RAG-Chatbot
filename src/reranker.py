from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("\n Loading Reranker Model...")
        print("Model : cross-encoder/ms-marco-MiniLM-L-6-v2")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print(" Reranker Loaded Successfully!")

    def rerank(self, query, documents, top_k=3):
        """
        Rerank retrieved documents using CrossEncoder.
        """

        print("\n Reranking Retrieved Chunks...")

        pairs = [
            (query, doc.page_content)
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(scores, documents),
            key=lambda x: x[0],
            reverse=True
        )

        print("\n========== RERANKED RESULTS ==========")

        final_docs = []

        for rank, (score, doc) in enumerate(ranked[:top_k], start=1):

            print(f"\nRank {rank}")
            print(f"Score : {score:.4f}")
            print("-" * 40)
            print(doc.page_content[:250])
            print("-" * 40)

            final_docs.append(doc)

        return final_docs