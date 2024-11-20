from ollama import Client

client = Client(host="http://localhost:11434")
response = client.chat(model="llama3.2", messages=[{"role": "user", "content": "What is 1 + 1?"}])
print(response.get("message").get("content"))