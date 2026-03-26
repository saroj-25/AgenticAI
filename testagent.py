import ollama

responses = ollama.chat(
    model = "gemma3:1b",
    messages = [{"role":"user", "content":"What is Agentic AI? "}]

)

# print(responses["message"]["content"])

print(responses.message.content)
