import ollama
import tomllib
from rich import print


class AIManager:
    def __init__(self):
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)

        self.chat_history = []  # Stores the entire conversation
        self.AI_MODEL = config["ollama"]["ai_model"]
        self.max_message_context = config["ollama"]["max_message_context"]

    def ask_question(self, messages):
        print("[yellow]\nAsking AI a question...")
        return ollama.chat(self.AI_MODEL, messages=messages)

    # Asks a question with no chat history
    def chat(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        chat_question = [{"role": "user", "content": prompt}]

        completion = self.ask_question(chat_question)

        # Process the answer
        ai_answer = completion["message"]["content"]
        print(f"[green]\n{ai_answer}\n")
        return ai_answer

    # Asks a question that includes the full conversation history
    def chat_with_history(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        # Add our prompt into the chat history
        self.chat_history.append({"role": "user", "content": prompt})

        # Check total token limit. Remove old messages as needed
        print(f"[coral]Chat History has a length of {len(self.chat_history)}")
        while len(self.chat_history) > self.max_message_context:
            # We skip the 1st message since it's the system message
            self.chat_history.pop(1)
            print(f"Popped a message! New context length is: {len(self.chat_history)}")

        completion = self.ask_question(self.chat_history)

        # Add this answer to our chat history
        self.chat_history.append(completion["message"])

        # Process the answer
        ai_answer = completion["message"]["content"]
        print(f"[green]\n{ai_answer}\n")
        return ai_answer
