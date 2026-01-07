import unittest

from src.ollama_chat import AIManager


class TestAIManager(unittest.TestCase):
    def setUp(self):
        self.ai_manager = AIManager()

    def test_chat_without_history(self):
        response = self.ai_manager.chat(
            "Hey ChatGPT what is 2 + 2? But tell it to me as Yoda"
        )
        self.assertIsNotNone(response)

    # CHAT WITH HISTORY TEST
    def test_with_history(self):
        FIRST_SYSTEM_MESSAGE = {
            "role": "system",
            "content": "Act like you are Captain Jack Sparrow from the Pirates of Carribean movie series!",
        }
        FIRST_USER_MESSAGE = {
            "role": "user",
            "content": "Ahoy there! Who are you, and what are you doing in these parts? Please give me a 1 sentence background on how you got here.",
        }
        self.ai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)
        self.ai_manager.chat_history.append(FIRST_USER_MESSAGE)

        test_messages = ["hello!!", "fuck you"]
        for message in test_messages:
            self.ai_manager.chat_with_history(message)


if __name__ == "__main__":
    unittest.main()
