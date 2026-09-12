import os
from dotenv import load_dotenv
from groq import Groq


class GroqLLM:
    """
    Groq LLM for generating answers
    using retrieved PDF context
    and conversation history.
    """

    FALLBACK_RESPONSE = "I couldn't find this information in the uploaded PDF."

    def __init__(self):

        load_dotenv()

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-120b"
        # llama-3.3-70b-versatile

        print("\n🤖 Loading Groq LLM...")
        print(f"Model : {self.model}")
        print("✅ Groq LLM Loaded Successfully!")

    def _fallback_response(self):
        return self.FALLBACK_RESPONSE

    def _build_prompt(self, context, question, memory=""):
        context_text = str(context or "").strip()
        memory_text = str(memory or "").strip()
        question_text = str(question or "").strip()

        return f"""
You are a grounded PDF QA assistant.

Instructions:
1. Use the retrieved context as the source of truth and answer using only the retrieved PDF context and the conversation history.
2. The retrieved context may be paraphrased or use different wording than the question; this is still valid if it contains the same fact or concept.
3. Semantic equivalence is valid: a paraphrase of the answer is acceptable if it preserves the original meaning.
4. Do NOT require the question's exact wording to appear in the context.
5. If the context contains enough information to answer the question, answer directly in a concise but complete way.
6. If the context is empty, irrelevant, or does not contain enough information to support an answer, reply exactly:
   "I couldn't find this information in the uploaded PDF."
7. Do not invent facts or add unsupported details.
8. If the answer is implied by the context, synthesize it in natural language without changing meaning.

==================================================

Conversation History

{memory_text}

==================================================

Retrieved Context

{context_text}

==================================================

Current Question

{question_text}

==================================================

Answer:
"""

    def generate_answer(
        self,
        context,
        question,
        memory=""
    ):
        """
        Generates an answer using:
        1. Conversation Memory
        2. Retrieved Context
        3. Current Question
        """

        if not str(context or "").strip():
            return self._fallback_response()

        prompt = self._build_prompt(
            context=context,
            question=question,
            memory=memory,
        )

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=0,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You answer ONLY using the uploaded PDFs and previous conversation. "
                        "Treat paraphrased or semantically equivalent context as valid. "
                        "If the context is insufficient, return the exact fallback sentence."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        answer = response.choices[0].message.content.strip()
        if not answer:
            return self._fallback_response()
        if answer.lower().startswith("i couldn't find this information in the uploaded pdf."):
            return self._fallback_response()
        return answer