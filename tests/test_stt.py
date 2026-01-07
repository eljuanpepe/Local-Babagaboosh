import unittest

from src.speech_to_text import SpeechToTextManager


class TestSpeachToText(unittest.TestCase):
    def setUp(self):
        self.speechtotext_manager = SpeechToTextManager()

    def test_microphone_audio_stream(self):
        result = self.speechtotext_manager.speechtotext_from_mic_continuous()
        print(f"\n\nHERE IS THE RESULT:\n{result}")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
