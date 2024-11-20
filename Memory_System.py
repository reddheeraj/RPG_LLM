class MemorySystem:
    def __init__(self, llm):
        """
        Initializes a simple memory system to store interactions and knowledge.
        """
        self.history = []  # Store interactions as a list of dictionaries
        self.conversation_chain = []
        self.llm = llm

    def load_memory(self):
        """
        Retrieve the entire memory history.
        """
        return self.history

    def save_context(self, inputs, outputs):
        """
        Save an interaction to memory.
        """
        self.history.append({"inputs": inputs, "outputs": outputs})

    def add_memory(self, new_info):
        """
        Add new knowledge or information to memory.
        """
        self.history.append({"knowledge": new_info})

    def clear(self):
        """
        Clear the memory.
        """
        self.history = []

    def get_last_n_memories(self, n):
        """
        Get the last N memories from the history.
        """
        return self.history[-n:]

    def update_conversation(self, dialogue):
        """
        Update conversation chain with new dialogue.
        """
        self.conversation_chain.append(dialogue)
    
    def get_conversation(self):
        """
        Get the current conversation as a string.
        """
        return " ".join(self.conversation_chain)
    
    def interact_with_agent(self, other_agent_name):
        """
        Generate a dialogue with another agent based on memory and conversation.
        """
        prompt = f"Talk to {other_agent_name} about your experiences and life. talk short, not long."
        dialogue = self._generate_dialogue(prompt)  # You can add an LLM call here to generate the conversation
        self.update_conversation(dialogue)
        return dialogue

    def _generate_dialogue(self, prompt):
        """
        Generate a dialogue response based on a prompt.
        """
        return self.llm.generate_action(prompt)
