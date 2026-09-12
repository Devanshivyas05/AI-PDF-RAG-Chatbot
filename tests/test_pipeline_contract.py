import unittest

from src.text_splitter import split_text
from src.tools import ToolManager


class SplitterContractTests(unittest.TestCase):
    def test_split_text_uses_text_blocks_to_create_documents(self):
        pdf = {
            "file_name": "sample.pdf",
            "content": [
                {
                    "page": 1,
                    "text_blocks": [
                        {"text": "Alpha beta gamma"},
                        {"text": "Delta epsilon zeta"},
                    ],
                    "tables": [],
                    "images": ["/tmp/original_image.png"],
                    "figures": [],
                    "page_image": "/tmp/page_image.png",
                }
            ],
        }

        documents = split_text(pdf)

        self.assertGreater(len(documents), 0)
        self.assertTrue(any(doc.metadata.get("type") == "text" for doc in documents))
        self.assertTrue(any(doc.metadata.get("type") == "image" for doc in documents))

        first_text_doc = next(doc for doc in documents if doc.metadata.get("type") == "text")
        self.assertEqual(first_text_doc.metadata["source"], "sample.pdf")
        self.assertEqual(first_text_doc.metadata["page"], 1)
        self.assertIn("Alpha", first_text_doc.page_content)

    def test_table_queries_use_the_table_tool(self):
        manager = ToolManager()
        self.assertEqual(manager.select_tool("Show confusion matrix"), "table")
        self.assertEqual(manager.select_tool("Show the accuracy table"), "table")


class LLMContractTests(unittest.TestCase):
    def test_prompt_allows_semantic_paraphrase_and_grounded_fallback(self):
        from src.llm import GroqLLM

        llm = GroqLLM.__new__(GroqLLM)
        prompt = llm._build_prompt(
            context="Supervised learning algorithms are trained using labeled data.",
            question="What is supervised learning?",
            memory="",
        )

        self.assertIn("semantic", prompt.lower())
        self.assertIn("paraphrase", prompt.lower())
        self.assertIn("use the retrieved context", prompt.lower())
        self.assertIn("I couldn't find this information in the uploaded PDF.", prompt)

    def test_empty_context_returns_grounded_fallback(self):
        from src.llm import GroqLLM

        llm = GroqLLM.__new__(GroqLLM)
        self.assertEqual(
            llm._fallback_response(),
            "I couldn't find this information in the uploaded PDF.",
        )


if __name__ == "__main__":
    unittest.main()
