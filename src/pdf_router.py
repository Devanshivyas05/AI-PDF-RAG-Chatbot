from collections import defaultdict


class PDFRouter:

    def __init__(self):
        pass

    def route(self, vector_db, query):

        print("\n Routing Question...")

        docs = vector_db.similarity_search(
            query,
            k=10
        )

        pdf_scores = defaultdict(int)

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "Unknown"
            )

            pdf_scores[source] += 1

        best_pdf = max(
            pdf_scores,
            key=pdf_scores.get
        )

        print(f" Selected PDF : {best_pdf}")

        return best_pdf