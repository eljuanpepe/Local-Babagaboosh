import unittest

from src.text_to_speech import TTSManager


class TTSTest(unittest.TestCase):
    def setUp(self):
        self.tts_manager = TTSManager()

    def test_audio_generation(self):
        file_path = self.tts_manager.text_to_audio(
            "This is my saved test audio, please make me beautiful"
        )
        self.assertIsNotNone(file_path)


if __name__ == "__main__":
    unittest.main()
