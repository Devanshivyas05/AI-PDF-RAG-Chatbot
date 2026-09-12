class ConversationMemory:
    """
    Stores conversation history
    between the user and the chatbot.
    """

    def __init__(self):

        self.history = []

    def add(self, question, answer):

        self.history.append({

            "question": question,

            "answer": answer

        })

    def get_context(self, last_n=3):
        """
        Returns the last few conversations.
        """

        if not self.history:
            return ""

        context = ""

        for chat in self.history[-last_n:]:

            context += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )

        return context

    def clear(self):

        self.history = []