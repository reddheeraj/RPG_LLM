from ollama import Client
from langchain_core.runnables import Runnable
from langchain.schema import AIMessage

class LLMIntegration:
    """
    This class integrates with the Ollama server to generate actions and reflections
    using LangChain-like functionality.
    """
    def __init__(self, server_url="http://localhost:11434"):
        self.server_url = server_url
        self.client = Client(host=server_url)

    def generate_action(self, prompt):
        """
        Sends a prompt to the local Ollama server and retrieves a response.
        """
        try:
            response = self.client.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
            
            return response.get("message").get("content")
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return None