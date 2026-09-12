class ToolManager:
    """
    Decides which tool should answer
    the user's question.
    """

    def __init__(self):
        pass

    def select_tool(self, question):

        question = question.lower()

        # -------------------------
        # Image Questions
        # -------------------------

        table_keywords = [

            "table",
            "tabular",
            "rows",
            "columns",
            "matrix",
            "confusion",
            "accuracy"

        ]

        # -------------------------
        # Image Questions
        # -------------------------

        image_keywords = [

            "image",
            "diagram",
            "figure",
            "picture",
            "flowchart",
            "graph",
            "architecture",
            "photo",
            "cnn",
            "ann",
            "decision tree",
            "tree"

        ]

        # -------------------------
        # Memory Questions
        # -------------------------

        memory_keywords = [

            "previous",
            "before",
            "last question",
            "earlier"

        ]

        for word in table_keywords:

            if word in question:

                return "table"

        for word in image_keywords:

            if word in question:

                return "image"

        for word in memory_keywords:

            if word in question:

                return "memory"

        return "retriever"